import json

from django.shortcuts import render
from rest_framework.views import APIView
from django.conf import settings

from .forms import PostUpdateForm, CommentForm, PostModelForm

User = settings.AUTH_USER_MODEL

from django.shortcuts import render, redirect
from .models import PostModel
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.core.paginator import (
   Paginator, EmptyPage,
   PageNotAnInteger
)
from .models import *
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    AllowAny,
)
from rest_framework.response import Response
from rest_framework import status
from .renderers import blogRenderer
from rest_framework.views import APIView
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    UpdateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView, get_object_or_404,
)
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from .renderers import blogRenderer
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter,OrderingFilter



def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
class CreatePostAPIView(APIView):


    queryset = PostModel.objects.all()
    serializer_class = PostCreateUpdateSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request, *args, **kwargs):
        serializer = PostCreateUpdateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save(author=request.user)
            token = get_tokens_for_user(user)
            draft = serializer.data.get("draft")
            if draft == True:
                return Response({'token':token,'msg':'post drafted succesfully'},status=status.HTTP_201_CREATED)
            else:
                return Response({'token':token,'msg':'post published succesfully'},status=status.HTTP_201_CREATED)
        else:
            return Response({"errors": serializer.errors}, status=400)

@api_view(['GET'])
def all_publised_listView(request):

    if request.method == 'GET':
        posts = PostModel.objects.filter(draft=False)
        serializer = PostListSerializer(posts, many=True)
        return Response(serializer.data)

class PaginationView(ListAPIView):
    queryset = PostModel.objects.filter(draft=False)
    serializer_class = PostListSerializer
    pagination_class = PageNumberPagination

class PaginationWithSearchView(ListAPIView):
    queryset = PostModel.objects.filter(draft=False)
    serializer_class = PostListSerializer
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter,OrderingFilter)
    search_fields = ('title','content','author__email')



@api_view(['GET'])
def all_post_listView(request):

    if request.method == 'GET':
        posts = PostModel.objects.all()
        serializer = PostListSerializer(posts, many=True)
        return Response(serializer.data)

class PostUpdateView(APIView):
  renderer_classes = [blogRenderer]
  permission_classes = [IsAuthenticated]
  def put(self, request,pk, format=None):
      try:
          post = PostModel.objects.get(pk=pk)
      except PostModel.DoesNotExist:
          return Response(status=status.HTTP_404_NOT_FOUND)

      serializer = updatePostSerializer(post, data=request.data)
      serializer.is_valid(raise_exception=True)
      serializer.save()
      return Response({'msg': 'post update succesfully'}, status=status.HTTP_200_OK)

class PostDeleteView(APIView):
  renderer_classes = [blogRenderer]
  permission_classes = [IsAuthenticated]
  def delete(self, request,pk, format=None):
      try:
          post = PostModel.objects.get(pk=pk)
      except PostModel.DoesNotExist:
          return Response(status=status.HTTP_404_NOT_FOUND)
      if post.author!=request.user:
          return Response({'msg': 'Not actual User'}, status=status.HTTP_200_OK)
      else:

          post.delete()
          return Response({'msg': 'post delete succesfully'}, status=status.HTTP_200_OK)



class CreateCommentAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]
    renderer_classes = [blogRenderer]

    def post(self, request,pk,*args, **kwargs):
        try:
            posts = PostModel.objects.get(pk=pk)
        except PostModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        post = PostModel.objects.get(pk=pk)
        postid = post.id

        serializer = CreatComment(post,data=request.data)
        if serializer.is_valid(raise_exception=True):
            print(post)
            print(request.user)
            try :
                serializer.save(user=request.user,post=post)
                serializer.create(validate_data=request.data)
                Comment.objects.create(user=request.user,post=post)
            except Exception as e:
                print(e)









        #Comment.objects.create(user=request.user, post=post)

        return Response(serializer.data)



       # return Response({'msg': 'comment  succesfully'},serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def post_View_with_Comment(request):

    if request.method == 'GET':
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


# front end view

@login_required
def index(request):
    posts = PostModel.objects.filter(draft=False)
    if request.method == 'POST':
        form = PostModelForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            return redirect('blog-index')
    else:
        form = PostModelForm()
    context = {
        'posts': posts,
        'form': form
    }

    return render(request, 'blog/index.html', context)


@login_required
def post_detail(request, pk):
    post = PostModel.objects.get(id=pk)
    if request.method == 'POST':
        c_form = CommentForm(request.POST)
        if c_form.is_valid():
            instance = c_form.save(commit=False)
            instance.user = request.user
            instance.post = post
            instance.save()
            return redirect('blog-post-detail', pk=post.id)
    else:
        c_form = CommentForm()
    context = {
        'post': post,
        'c_form': c_form,
    }
    return render(request, 'blog/post_detail.html', context)


@login_required
def post_edit(request, pk):
    post = PostModel.objects.get(id=pk)
    if request.method == 'POST':
        form = PostUpdateForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog-post-detail', pk=post.id)
    else:
        form = PostUpdateForm(instance=post)
    context = {
        'post': post,
        'form': form,
    }
    return render(request, 'blog/post_edit.html', context)


@login_required
def post_delete(request, pk):
    post = PostModel.objects.get(id=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('blog-index')
    context = {
        'post': post
    }
    return render(request, 'blog/post_delete.html', context)