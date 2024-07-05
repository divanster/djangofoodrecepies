from django.urls import path
from .views import RegisterView, ProfilePageView, logout_view

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/<slug:username>/', ProfilePageView.as_view(), name='profile'),
    path('logout/', logout_view, name='logout'),
]
