# api/urls.py
from django.urls import path
from .views import ItemList, ItemDetail, CommentListCreateView, CommentDeleteView, ApiRootView, RegisterView, LoginView, RatingSubmitView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('', ApiRootView.as_view(), name='api-root'),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('items/', ItemList.as_view(), name='item-list'),
    path('items/<int:pk>/', ItemDetail.as_view(), name='item-detail'),
    path('items/<int:item_id>/comments/', CommentListCreateView.as_view(), name='item-comments'),
    path('comments/<int:pk>/', CommentDeleteView.as_view(), name='comment-delete'),
    path('items/<int:pk>/rate/', RatingSubmitView.as_view(), name='item-rate'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
