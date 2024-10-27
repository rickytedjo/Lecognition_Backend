from rest_framework import serializers
from api.models import *
import hashlib
from django.conf import settings
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        validated_data['password'] = hashlib.sha256((validated_data['password']+settings.SECRET_KEY).encode('utf-8')).hexdigest()
        return super(UserSerializer, self).create(validated_data)

class SafeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username']


class AuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email','password']

class DiseaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disease
        fields = '__all__'

class GetScanSerializer(serializers.ModelSerializer):
    user = SafeUserSerializer()
    diagnosis = DiseaseSerializer()

    class Meta:
        model = Scan
        fields = '__all__'

class ScanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scan
        fields = '__all__'

class GetBookmarkSerializer(serializers.ModelSerializer):
    user = SafeUserSerializer()
    disease = DiseaseSerializer()

    class Meta:
        model = Bookmark
        fields = '__all__'

class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = '__all__'
