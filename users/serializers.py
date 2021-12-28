from rest_framework import serializers
from users.models import CustomUser, Store
from django.contrib.auth.hashers import make_password
from product_uploader_api.custompermission import ADMIN, SUPER_ADMIN


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = 'CustomUserSerializer'
        model = CustomUser
        fields = '__all__'


class PublicUserSerializer(serializers.ModelSerializer):

    class Meta:
        ref_name = 'CustomUserSerializer'
        model = CustomUser
        fields = ['id', 'email', 'first_name',
                  'last_name', 'username', 'role', 'password', 'wp_username', 'wp_password']

    def validate(self, data):
        user = None
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
        else:
            raise serializers.ValidationError({
                'error_code': 'unauthenticate',
                'detail': 'You need to login'
            }, code=401)
        if user and (user.role <= data.get('role', 1) and user.role != SUPER_ADMIN and user.role != ADMIN):
            raise serializers.ValidationError(
                {"role": ["You can\'t not create or update a new user with higher privilege"]})
        return data

    def create(self, validated_data):
        plain_password = validated_data.get('password')
        encoded_password = make_password(plain_password)
        validated_data['password'] = encoded_password
        return super().create(validated_data)

    def update(self, instance, validated_data):
        user = None
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
        if user.id != instance.id and user.role != SUPER_ADMIN:
            raise serializers.ValidationError(
                {"role": [
                    "You can\'t not create or update a new user with higher privilege"]}
            )
        plain_password = validated_data.get('password')
        encoded_password = make_password(plain_password)
        validated_data['password'] = encoded_password
        return super().update(instance, validated_data)


class PublicUserForViewSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = 'CustomUserSerializer'
        model = CustomUser
        fields = ['id', 'email', 'first_name',
                  'last_name', 'username', 'role', 'wp_username', 'wp_password']


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'


class StoreViewSerializer(serializers.ModelSerializer):
    users = PublicUserSerializer(many=True)

    class Meta:
        model = Store
        fields = '__all__'
