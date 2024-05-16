from django.urls import path, include
from . import views



app_name = 'food'
urlpatterns = [
    # /food/
    path('', views.IndexClassView.as_view(), name='index'),
    # /food/1
    path('<int:pk>/', views.FoodDetail.as_view(), name='detail'),
    path('item/', views.item, name='item'),
    # add items
    path('add/', views.CreateItem.as_view(), name='create_item'),
    # edit
    path('update/<int:item_id>/', views.update_item, name='update_item'),
    # delete
    path('delete/<int:item_id>/', views.delete_item, name='delete_item'),
    # rating
    path('<int:pk>/submit_rating/', views.submit_rating, name='submit_rating'),
    # comments
    path('<int:pk>/add_comment/', views.add_comment, name='add_comment'),
    path('<int:item_pk>/delete_comment/<int:comment_pk>/', views.delete_comment, name='delete_comment'),



    path('404/', views.handler404, name='error_404'),
    path('500/', views.handler500, name='error_500'),



]
