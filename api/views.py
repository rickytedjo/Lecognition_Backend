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

def decode_token(request):
    try:
        if request and request.startswith('Bearer '):
            # Extract the token part
            token = request.split(' ')[1]
            return token
        return Response('No Authorization')
    except Exception as e:
        print("Token decoding error:", e)

def get_id_from_token(token):
    try:
        if token:
            decoded_token = AccessToken(token)
            user_id = decoded_token['user_id']
            return user_id
        return Response('No Authorization')
    except Exception as e:
         print("Token decoding error:", e)

@api_view(['GET','POST','PUT','DELETE'])
@parser_classes([FormParser, MultiPartParser, JSONParser])
def user_api(request, id=None):
    token = decode_token(request.headers.get('Authorization'))
    user_id = get_id_from_token(token)
    if token is not None:
        if (request.method == 'GET') & (id == None):
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)
        
        if (request.method == 'GET') & (id != None):
            try:    
                users = User.objects.get(id = id)
                serializer = UserSerializer(users)
                return Response(serializer.data)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        if (request.method == 'PUT'):
            try:
                instance = User.objects.get(id = id)
                serializer = UserSerializer(instance, data = request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response('Data Updated', status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        if (request.method == 'DELETE'):
            try:
                instance = User.objects.get(id = id)
                instance.delete()
                return Response('Data Deleted',status=status.HTTP_204_NO_CONTENT)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET','POST','PUT','DELETE'])
@parser_classes([FormParser, MultiPartParser])
def disease_api(request, id=None):
    token = decode_token(request.headers.get('Authorization'))
    user_id = get_id_from_token(token)
    if token is not None:
        if (request.method == 'GET') & (id == None):
            disease = Disease.objects.all()
            serializer = DiseaseSerializer(disease, many=True)
            return Response(serializer.data)
        if (request.method == 'GET') & (id != None):
            disease = Disease.objects.get(id = id)
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
                instance = Disease.objects.get(id = id)
                serializer = DiseaseSerializer(instance, data= request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response('Data Updated', status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        if (request.method == 'DELETE'):
            try:
                instance = Disease.objects.get(id = id)
                instance.delete()
                return Response('Data Deleted',status=status.HTTP_204_NO_CONTENT)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET','POST','PUT','DELETE'])
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
            scan = Scan.objects.get(id = id)
            serializer = GetScanSerializer(scan)
            return Response(serializer.data)
        
        ## GET

        if (request.method == 'DELETE'):
            try:
                instance = Scan.objects.get(id = id)
                instance.delete()
                return Response('Data Deleted',status=status.HTTP_204_NO_CONTENT)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

@api_view(['GET','POST','PUT','DELETE'])
@parser_classes([FormParser, MultiPartParser])
def bookmark_api(request, id=None):
    token = decode_token(request.headers.get('Authorization'))
    user_id = get_id_from_token(token)
    if token is not None:
        if (request.method == 'GET') & (id == None):
            bookmark = Bookmark.objects.all()
            serializer = GetBookmarkSerializer(bookmark, many=True)
            return Response(serializer.data)
        if (request.method == 'GET') & (id != None):
            bookmark = Bookmark.objects.get(id = id)
            serializer = GetBookmarkSerializer(bookmark)
            return Response(serializer.data)
        if (request.method == 'POST'):
            try:
                serializer = BookmarkSerializer(data = request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response('Data Created', status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        if (request.method == 'DELETE'):
            try:
                instance = Bookmark.objects.get(id = id)
                instance.delete()
                return Response('Data Deleted',status=status.HTTP_204_NO_CONTENT)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@parser_classes([FormParser, MultiPartParser])
def login(request):
    if (request.method == 'POST'): ## Login
        try:
            serializer = AuthSerializer(data=request.data)
            if serializer.is_valid():
                email = serializer.validated_data['email']
                password = hashlib.sha256((serializer.validated_data['password'] + settings.SECRET_KEY).encode('utf-8')).hexdigest()
                try:
                    user = User.objects.get(email=email, password=password)
                except User.DoesNotExist:
                    return Response({'error': 'Invalid email or password'}, status=status.HTTP_404_NOT_FOUND)
                if user:
                    refresh = RefreshToken.for_user(user)
                    access_token = str(refresh.access_token)
                    return Response({
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),  # Generate access from refresh
                    }, status=status.HTTP_200_OK)
                return Response({'error': 'Invalid email or password'}, status=status.HTTP_404_NOT_FOUND)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

@api_view(['POST'])
@parser_classes([FormParser, MultiPartParser])
def register(request):
    if (request.method == 'POST'):
        try:
            serializer = UserSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response('Data Created', status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)