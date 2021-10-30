from rest_framework import serializers
from users.models import CustomUser, Store
from django.contrib.auth.hashers import make_password


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
                  'last_name', 'username', 'role', 'password']

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
        if user and user.role <= data.get('role', 1):
            raise serializers.ValidationError(
                {"role": ["You can\'t not create a new user with higher privilege"]})
        return data

    def create(self, validated_data):
        plain_password = validated_data.get('password')
        encoded_password = make_password(plain_password)
        validated_data['password'] = encoded_password
        return super().create(validated_data)

    def update(self, instance, validated_data):
        plain_password = validated_data.get('password')
        encoded_password = make_password(plain_password)
        validated_data['password'] = encoded_password
        return super().update(instance, validated_data)


class PublicUserForViewSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = 'CustomUserSerializer'
        model = CustomUser
        fields = ['id', 'email', 'first_name',
                  'last_name', 'username', 'role']


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'


class StoreViewSerializer(serializers.ModelSerializer):
    users = PublicUserSerializer(many=True)

    class Meta:
        model = Store
        fields = '__all__'
