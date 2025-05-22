from rest_framework import serializers
from .models import *


class CustomUserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUserModel
        fields = ('id','username', 'email', 'password', 'details')
        
class CustomUserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUserDetails
        fields = "__all__"

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUserModel
        fields = ("username", "password")
        
        
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
        