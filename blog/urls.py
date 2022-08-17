from django.urls import path
from .views import *
from .import views
urlpatterns = [
    path('createpostapi/',CreatePostAPIView.as_view(), name='createpostApi'),
    path('allpublishedlist/',views.all_publised_listView),
    path('allpostlist/',views.all_post_listView),
    path('updatepost/<pk>/',PostUpdateView.as_view()),
    path('pageination/',PaginationView.as_view()),
    path('search/',PaginationWithSearchView.as_view()),
    path('deletepost/<pk>/',PostDeleteView.as_view()),
    path('createcomment/<pk>/',CreateCommentAPIView.as_view(), name='createcomment'),
    path('allcommentforapost/',views.post_View_with_Comment),
    path('blog/', views.index, name='blog-index'),
    path('post_detail/<int:pk>/', views.post_detail, name='blog-post-detail'),
    path('post_edit/<int:pk>/', views.post_edit, name='blog-post-edit'),
    path('post_delete/<int:pk>/', views.post_delete, name='blog-post-delete'),




]