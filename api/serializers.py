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
    user_name = serializers.ReadOnlyField(source='user_name.username')
    get_average_rating = serializers.ReadOnlyField()

    class Meta:
        model = Item
        fields = ['id', 'item_name', 'item_desc', 'item_image', 'views', 'user_name', 'get_average_rating']


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    item = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all())

    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_at', 'user', 'item']


class RatingSerializer(serializers.Serializer):
    rating = serializers.IntegerField()

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value
