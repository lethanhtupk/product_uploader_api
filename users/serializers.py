from rest_framework import serializers
from users.models import CustomUser, Store


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = 'CustomUserSerializer'
        model = CustomUser
        fields = '__all__'


class PublicUserSerializer(serializers.ModelSerializer):

    class Meta:
        ref_name = 'CustomUserSerializer'
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'username']


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'


class StoreViewSerializer(serializers.ModelSerializer):
    users = PublicUserSerializer(many=True)

    class Meta:
        model = Store
        fields = '__all__'
