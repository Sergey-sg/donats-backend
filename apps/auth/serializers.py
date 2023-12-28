from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from django.contrib.auth.models import update_last_login

from apps.user.models import User, VolunteerInfo
from apps.user.serializers import UserSerializer


class CustomProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = VolunteerInfo
        fields = ['public_name', 'first_name', 'last_name', 'additional_info']


class UserRegistrationSerializer(serializers.ModelSerializer):
    user = CustomProfileSerializer(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'user']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data, password=password)
        volunteer_info = VolunteerInfo.objects.create(user=user, **user_data)
        return user
    

class UserLoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['user'] = UserSerializer(self.user).data
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)
        return data
