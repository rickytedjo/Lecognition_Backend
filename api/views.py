from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import parser_classes
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from api.models import *
from api.serializers import *
from django.http import Http404
from keras.models import load_model
import cv2 as cv
import numpy as np
from PIL import Image
from io import BytesIO
import base64
import os
from keras.utils import to_categorical
from sklearn.preprocessing import LabelEncoder; label_encoder = LabelEncoder()
from decimal import Decimal, getcontext

DATA_DIR = 'dataset'
IMG_SIZE = (224,224)


def load_data(data_dir):
    images, labels = [], []
    for label in os.listdir(data_dir):
        class_dir = os.path.join(data_dir, label)
        if os.path.isdir(class_dir):
            for file in os.listdir(class_dir):
                img_path = os.path.join(class_dir, file)
                img = cv.imread(img_path)
                if img is not None:
                    img = cv.resize(img, IMG_SIZE)
                    images.append(img)
                    labels.append(label)
    return np.array(images), np.array(labels)

# Muat data
X, y = load_data(DATA_DIR)

# Encoding label
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)
y_categorical = to_categorical(y_encoded)

model = load_model('saved_model')

def prediction(image):
    if image is None:
        print(f"Error: Image not found")
        return None

    img_resized = cv.resize(image, (224,224))
    img_array = np.expand_dims(img_resized, axis=0)

    prediction = model.predict(img_array)
    predicted_class = np.argmax(prediction, axis=1)[0]
    disease_name = label_encoder.classes_[predicted_class]
    confidence = np.max(prediction)

    return disease_name, confidence

def match(image, threshold=0.5):
    image = cv.cvtColor(image, cv.COLOR_RGB2BGR)
    image_gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    
    templates = os.listdir('../asset/comparator')
    for template in templates:
        template_img = cv.imread('../asset/comparator/' + str(template))
        template_img = cv.cvtColor(template_img,cv.COLOR_RGB2BGR)
        template_gray = cv.cvtColor(template_img, cv.COLOR_BGR2GRAY)

        h, w = template_gray.shape
       
        image_gray = cv.resize(image_gray, (w, h))
        resized_template = cv.resize(template_gray, (w, h))

        res = cv.matchTemplate(image_gray, resized_template, cv.TM_CCOEFF_NORMED)
        res_copy = res.copy()

        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res_copy)
        # Search threshold
        if max_val >= threshold:
            return True

    return False



def decode_token(request):
    try:
        if request and request.startswith('Bearer '):
            # Extract the token part
            token = request.split(' ')[1]
            return token
        else:
            return Response('No Authorization')
    except Exception as e:
        print("Token decoding error:", e)


def get_id_from_token(token):
    try:
        if token:
            decoded_token = AccessToken(token)
            print(decoded_token)
            user_id = decoded_token['user_id']
            print(user_id)
            return user_id
        else:
            return Response('No Authorization')
    except Exception as e:
        print("Token decoding error:", e)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@parser_classes([FormParser, MultiPartParser, JSONParser])
def user_api(request, id=None):
    print(request.headers)
    token = decode_token(request.headers.get('Authorization'))
    user_id = get_id_from_token(token)
    if token is not None:
        if (request.method == 'GET') & (id == None):
            try:
                user = User.objects.get(id=user_id)
                serializer = UserSerializer(user)
                return Response(serializer.data)
            except Exception as e:
                print(e)
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if (request.method == 'GET') & (id != None):
            try:
                users = User.objects.get(id=id)
                serializer = UserSerializer(users)
                return Response(serializer.data)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if (request.method == 'PUT'):
            try:
                instance = User.objects.get(
                    id=id) if id != None else User.objects.get(id=user_id)
                serializer = UserSerializer(
                    instance, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response('Data Updated', status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                print("error :", e)
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if (request.method == 'DELETE') & (id != None):
            try:
                instance = User.objects.get(id=id)
                instance.delete()
                return Response('Data Deleted', status=status.HTTP_204_NO_CONTENT)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@parser_classes([FormParser, MultiPartParser, JSONParser])
def user_all_api(request):
    token = decode_token(request.headers.get('Authorization'))
    if token is not None:
        if (request.method == 'GET'):
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)
    else:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@parser_classes([FormParser, MultiPartParser, JSONParser])
def disease_api(request, id=None):
    print(request.headers)
    token = decode_token(request.headers.get('Authorization'))
    print(token)
    user_id = get_id_from_token(token)
    if token is not None:
        if (request.method == 'GET') & (id == None):
            disease = Disease.objects.all()
            serializer = DiseaseSerializer(disease, many=True)
            return Response(serializer.data)
        if (request.method == 'GET') & (id != None):
            disease = Disease.objects.get(id=id)
            serializer = DiseaseSerializer(disease)
            return Response(serializer.data)
        if (request.method == 'POST'):
            try:
                serializer = DiseaseSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response('Data Created', status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        if (request.method == 'PUT'):
            try:
                instance = Disease.objects.get(id=id)
                serializer = DiseaseSerializer(
                    instance, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response('Data Updated', status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if (request.method == 'DELETE'):
            try:
                instance = Disease.objects.get(id=id)
                instance.delete()
                return Response('Data Deleted', status=status.HTTP_204_NO_CONTENT)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@parser_classes([FormParser, MultiPartParser])
def user_scans_api(request):
    token = decode_token(request.headers.get('Authorization'))
    user_id = get_id_from_token(token)
    if token is not None:
        if (request.method == 'GET'):
            scan = Scan.objects.all().filter(user_id=user_id)
            serializer = GetScanSerializer(scan, many=True)
            return Response(serializer.data)
    else:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@parser_classes([FormParser, MultiPartParser])
def scan_api(request, id=None):
    token = decode_token(request.headers.get('Authorization'))
    user_id = get_id_from_token(token)
    if token is not None:
        if (request.method == 'GET') & (id == None):
            scan = Scan.objects.all()
            serializer = GetScanSerializer(scan, many=True)
            return Response(serializer.data)
        if (request.method == 'GET') & (id != None):
            scan = Scan.objects.get(id=id)
            serializer = GetScanSerializer(scan)
            return Response(serializer.data)

        # POST
        if (request.method == 'POST'):
            try:
                data = request.data.copy()
                if data['img'] is not None:
                    uploaded_file = request.FILES.get("img")
                    if not uploaded_file:
                        return Response({"error": "No image file provided"}, status=400)

                    try:
                        # Read the raw byte data from the uploaded file
                        image_data = uploaded_file.read()

                        # Open the byte data as a PIL Image
                        image = Image.open(BytesIO(image_data))

                        # Convert the image to a NumPy array if needed
                        image_array = np.array(image)
                        # Detect Leaf
                        isleaf = match(image_array)
                        if isleaf is not True:
                            return Response({"error":"Gambar bukan daun"},status=status.HTTP_406_NOT_ACCEPTABLE)
                        disease_name, confidence = prediction(image_array)
                        disease = Disease.objects.filter(name__icontains=disease_name).first()
                        print(disease_name)
                        print(confidence)
                        if disease.id is None:
                            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
                        data['user'] = user_id
                        data['desc'] = ''
                        data['disease'] = disease.id
                        data['accuracy'] = float("{:.2f}".format(round(confidence * 100, 2)))
                        #data['datetime'] = 
                        serializer = ScanSerializer(data=data)
                        if serializer.is_valid():
                            serializer.save()
                            return Response({"disease":disease.id,"accuracy":confidence},status=status.HTTP_200_OK)
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                    except Exception as e:
                        return Response({"error": str(e)}, status=400)

                # data['user'] = user_id
                # serializer = ScanSerializer(data=data)
                # if serializer.is_valid():
                #     serializer.save()
                #     return Response('Data Created', status=status.HTTP_201_CREATED)
                # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # PUT - HANYA UNTUK DESC, DATA KOLOM LAIN TIDAK DIMAKSUD UNTUK DIGANTI
        if (request.method == 'PUT'):
            try:
                instance = Scan.objects.get(id=id)
                serializer = ScanSerializer(
                    instance, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response('Data Updated', status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if (request.method == 'DELETE'):
            try:
                instance = Scan.objects.get(id=id)
                # Delete image from storage
                instance.delete()
                return Response('Data Deleted', status=status.HTTP_204_NO_CONTENT)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@parser_classes([FormParser, MultiPartParser])
def user_bookmark_api(request):
    token = decode_token(request.headers.get('Authorization'))
    user_id = get_id_from_token(token)
    if token is not None:
        if (request.method == 'GET'):
            bookmark = Bookmark.objects.all().filter(user_id=user_id)
            serializer = GetBookmarkSerializer(bookmark, many=True)
            return Response(serializer.data)
    else:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@parser_classes([FormParser, MultiPartParser, JSONParser])
def bookmark_api(request, id=None):
    token = decode_token(request.headers.get('Authorization'))
    user_id = get_id_from_token(token)
    if token is not None:
        if (request.method == 'GET') & (id == None):
            bookmark = Bookmark.objects.all()
            serializer = GetBookmarkSerializer(bookmark, many=True)
            return Response(serializer.data)
        if (request.method == 'GET') & (id != None):
            bookmark = Bookmark.objects.get(id=id)
            serializer = GetBookmarkSerializer(bookmark)
            return Response(serializer.data)
        if (request.method == 'POST'):
            try:
                data = request.data.copy()
                data['user'] = user_id
                serializer = BookmarkSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                print("Yey error", e)
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        if (request.method == 'DELETE'):
            try:
                instance = Bookmark.objects.get(id=id)
                instance.delete()
                return Response('Data Deleted', status=status.HTTP_204_NO_CONTENT)
            except Exception as e:
                print("Yey error", e)
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    else:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@parser_classes([FormParser, MultiPartParser, JSONParser])
def login(request):
    if (request.method == 'POST'):  # Login
        try:
            serializer = AuthSerializer(data=request.data)
            if serializer.is_valid():
                email = serializer.validated_data['email']
                password = hashlib.sha256(
                    (serializer.validated_data['password'] + settings.SECRET_KEY).encode('utf-8')).hexdigest()
                try:
                    user = User.objects.get(email=email, password=password)
                except User.DoesNotExist:
                    return Response({'error': 'Invalid email or password'}, status=status.HTTP_404_NOT_FOUND)
                if user:
                    refresh = RefreshToken.for_user(user)
                    access_token = str(refresh.access_token)
                    return Response({
                        'refresh': str(refresh),
                        # Generate access from refresh
                        'access': str(refresh.access_token),
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Invalid email or password'}, status=status.HTTP_404_NOT_FOUND)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@parser_classes([FormParser, MultiPartParser, JSONParser])
def register(request):
    if (request.method == 'POST'):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response('Data Created', status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
