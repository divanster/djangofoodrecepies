from rest_framework import serializers
from django.contrib.auth.models import User
from food.models import Item, Comment


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class ItemSerializer(serializers.ModelSerializer):
    user_name = UserSerializer(read_only=True)

    class Meta:
        model = Item
        fields = ['id', 'item_name', 'item_desc', 'item_image', 'views', 'user_name', 'get_average_rating']


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_at', 'user', 'item']
