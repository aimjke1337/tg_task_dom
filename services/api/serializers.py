from rest_framework import serializers
from accounts.models import User
from services.models import Service, Request, Client

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name', 'description', 'price', 'form_schema']

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'full_name', 'telegram_username', 'phone', 'address', 'user']

class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ['id', 'client', 'service', 'data', 'status', 'created_at', 'executor']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'is_support', 'is_staff', 'is_superuser']
