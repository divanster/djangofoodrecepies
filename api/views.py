import logging
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, permissions, filters
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.views import View
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.contenttypes.models import ContentType
from star_ratings.models import Rating, UserRating

from .serializers import ItemSerializer, CommentSerializer, UserSerializer, RatingSerializer
from food.models import Item, Comment

logger = logging.getLogger(__name__)


class ApiRootView(View):
    def get(self, request):
        return JsonResponse({"message": "API Root. Access specific endpoints like /items/ or /comments/."})


class ItemList(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user_name', 'item_name']
    search_fields = ['item_name', 'item_desc']
    ordering_fields = ['views', 'item_name']

    def perform_create(self, serializer):
        serializer.save(user_name=self.request.user)


class ItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        item_id = self.kwargs['item_id']
        return Comment.objects.filter(item_id=item_id)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, item_id=self.kwargs['item_id'])


class CommentDeleteView(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()


class LoginView(generics.GenericAPIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            return Response({"error": "Username and password are required"},
                            status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        return Response({"error": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class RatingSubmitView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        logger.debug(f"Received rating submission for item {pk} with data: {request.data}")
        serializer = RatingSerializer(data=request.data)
        if serializer.is_valid():
            rating_value = serializer.validated_data['rating']
            try:
                item = get_object_or_404(Item, pk=pk)
                content_type = ContentType.objects.get_for_model(Item)
                rating, _ = Rating.objects.get_or_create(
                    content_type=content_type,
                    object_id=item.id,
                )
                UserRating.objects.update_or_create(
                    user=request.user,
                    rating=rating,
                    defaults={'score': rating_value}
                )
                logger.debug(f"Rating submitted successfully for item {pk}")
                return Response({'success': 'Rating submitted successfully'})
            except Exception as e:
                logger.error(f"Error submitting rating for item {pk}: {str(e)}")
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        logger.error(f"Invalid rating data for item {pk}: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
