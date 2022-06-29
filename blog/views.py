from django.shortcuts import render, redirect
from .models import PostModel
from .forms import PostModelForm, PostUpdateForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import (
   Paginator, EmptyPage,
   PageNotAnInteger
)
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    AllowAny,
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    UpdateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from .serializers import PostCreateUpdateSerializer,PostListSerializer,CommentSerializer,CommentCreateUpdateSerializer,UpdateSerialzation
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# api views here
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
            return Response({'token':token,'msg':'post created succesfully'},status=status.HTTP_201_CREATED)
        else:
            return Response({"errors": serializer.errors}, status=400)


@api_view(['GET', 'POST'])
def all_list(request):

    if request.method == 'GET':
        posts = PostModel.objects.all()
        serializer = PostListSerializer(posts, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PostListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def post_detail(request, pk):

    try:
        posts = PostModel.objects.get(pk=pk)
    except PostModel.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PostListSerializer(posts, many=True)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UpdateSerialzation(posts, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        posts.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



# Create your views here.

@login_required
def index(request):
    posts = PostModel.objects.all()
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

def post_list(request):
   object_list =  PostModel.objects.all()
   print(object_list.count())
   if request.method == 'POST':
       form = PostModelForm(request.POST)
       if form.is_valid():
           instance = form.save(commit=False)
           instance.author = request.user
           instance.save()
           return redirect('blog-index')
   else:
       form = PostModelForm()
   paginator = Paginator(object_list, 2) # 2 posts in each page
   page = request.GET.get('page')
   try:
       posts = paginator.page(page)
   except PageNotAnInteger:
       # If page is not an integer deliver the first page
       posts = paginator.page(1)
   except EmptyPage:
       # If page is out of range deliver last page of results
       posts = paginator.page(paginator.num_pages)
   return render(request,
                 'blog/index.html',
                 {'page': page,
                  'posts': posts,
                  'form': form})