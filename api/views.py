from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import parser_classes
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from api.models import *
from api.serializers import *
from django.http import Http404


# Create your views here.

@api_view(['GET','POST','PUT','DELETE'])
@parser_classes([FormParser, MultiPartParser, JSONParser])
def user_api(request, id=None):
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

    if (request.method == 'POST'):
        try:
            serializer = UserSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response('Data Created', status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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
    if (request.method == 'GET') & (id == None):
        scan = Scan.objects.all()
        serializer = ScanSerializer(scan, many=True)
        return Response(serializer.data)
    if (request.method == 'GET') & (id != None):
        scan = Scan.objects.get(id = id)
        serializer = ScanSerializer(scan)
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
    if (request.method == 'GET') & (id == None):
        bookmark = Bookmark.objects.all()
        serializer = BookmarkSerializer(bookmark, many=True)
        return Response(serializer.data)
    if (request.method == 'GET') & (id != None):
        bookmark = Bookmark.objects.get(id = id)
        serializer = BookmarkSerializer(bookmark)
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

