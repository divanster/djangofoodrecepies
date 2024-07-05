# from django.test import TestCase
# from django.contrib.auth.models import User
# from food.models import Item, Comment
# from api.serializers import UserSerializer, ItemSerializer, CommentSerializer, RatingSerializer
#
#
# class UserSerializerTest(TestCase):
#     def test_create_user(self):
#         data = {'username': 'testuser', 'email': 'testuser@example.com', 'password': 'testpass123'}
#         serializer = UserSerializer(data=data)
#         self.assertTrue(serializer.is_valid())
#         user = serializer.save()
#         self.assertEqual(user.username, data['username'])
#         self.assertEqual(user.email, data['email'])
#         self.assertTrue(user.check_password(data['password']))
#
#
# class ItemSerializerTest(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(username='testuser', password='testpass123')
#         self.item = Item.objects.create(item_name='Test Item', item_desc='Test Description', user_name=self.user)
#
#     def test_item_serialization(self):
#         serializer = ItemSerializer(self.item)
#         self.assertEqual(serializer.data['item_name'], 'Test Item')
#         self.assertEqual(serializer.data['item_desc'], 'Test Description')
#
#
# class CommentSerializerTest(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(username='testuser', password='testpass123')
#         self.item = Item.objects.create(item_name='Test Item', item_desc='Test Description', user_name=self.user)
#         self.comment = Comment.objects.create(content='Test Comment', user=self.user, item=self.item)
#
#     def test_comment_serialization(self):
#         serializer = CommentSerializer(self.comment)
#         self.assertEqual(serializer.data['content'], 'Test Comment')
#
#
# class RatingSerializerTest(TestCase):
#     def test_validate_rating(self):
#         serializer = RatingSerializer(data={'rating': 5})
#         self.assertTrue(serializer.is_valid())
#         self.assertEqual(serializer.validated_data['rating'], 5)
