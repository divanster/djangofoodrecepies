from rest_framework import serializers
from food.models import Item, Comment
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class ItemSerializer(serializers.ModelSerializer):
    user_name = UserSerializer()

    class Meta:
        model = Item
        fields = ['id', 'item_name', 'item_desc', 'item_image', 'views', 'user_name', 'get_average_rating']


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_at', 'user', 'item']
