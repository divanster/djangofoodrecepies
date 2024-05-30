from django.urls import path
from . import views
from .views import CommentDeleteView, SubmitRatingView


app_name = 'food'

urlpatterns = [
    path('', views.IndexClassView.as_view(), name='index'),
    path('<int:pk>/', views.FoodDetail.as_view(), name='detail'),
    path('add/', views.CreateItem.as_view(), name='create_item'),
    path('update/<int:pk>/', views.UpdateItem.as_view(), name='update_item'),
    path('delete/<int:pk>/', views.DeleteItem.as_view(), name='delete_item'),
    path('items/<int:pk>/submit_rating/', SubmitRatingView.as_view(), name='submit_rating'),
    # path('items/<int:pk>/submit_rating/', views.submit_rating, name='submit_rating'),
    path('<int:pk>/add_comment/', views.AddComment.as_view(), name='add_comment'),
    path('comments/<int:item_pk>/<int:pk>/delete/', CommentDeleteView.as_view(), name='delete_comment'),
    # path('<int:item_pk>/delete_comment/<int:comment_pk>/', views.delete_comment, name='delete_comment'),
    path('404/', views.handler404, name='error_404'),
    path('500/', views.handler500, name='error_500'),
]
