from django.urls import path
from .import views
from blog.views import CreatePostAPIView,post_list,post_detail

urlpatterns = [
    path('', views.post_list, name='blog-index'),
    path('post_detail/<int:pk>/', views.post_detail, name='blog-post-detail'),
    path('post_edit/<int:pk>/', views.post_edit, name='blog-post-edit'),
    path('post_delete/<int:pk>/', views.post_delete, name='blog-post-delete'),
    path('createpostapi/',CreatePostAPIView.as_view(), name='createpostApi'),
    path('allpostapi/',views.all_list, name='listpostApi'),
    path('posts/<int:pk>', views.post_detail)
]

