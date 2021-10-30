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
        fields = ['id', 'email', 'first_name',
                  'last_name', 'username', 'role']

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


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'


class StoreViewSerializer(serializers.ModelSerializer):
    users = PublicUserSerializer(many=True)

    class Meta:
        model = Store
        fields = '__all__'
