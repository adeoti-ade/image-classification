from rest_framework import serializers
from users.models import User, Token
from users.services.token import TokenService


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ["token"]
        extra_kwargs = {"token": {"required": True}}

    def validate(self, data):
        token = data.get("token", None)
        token_qs = Token.objects.filter(token=token)
        if not token_qs.exists():
            raise serializers.ValidationError(detail={
                "otp": "token does not exist"
            })

        return data


