from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, Goods

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'password2', 'is_blacklisted')
        read_only_fields = ('is_blacklisted',)

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'is_blacklisted')
        read_only_fields = ('username',)
        
    def __init__(self, *args, **kwargs):
        super(UserProfileSerializer, self).__init__(*args, **kwargs)
        user = self.context.get('request').user if self.context.get('request') else None
        if not user or not user.is_superuser:
            self.fields['is_blacklisted'].read_only = True

class GoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goods
        fields = ('id', 'title', 'price', 'img_url')

class UserPurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goods
        fields = ('id', 'title', 'price', 'img_url')
