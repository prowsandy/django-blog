from home.models import User
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from django.db.models import Q
from rest_framework.generics import ListAPIView,RetrieveAPIView,ListCreateAPIView
from rest_framework.views import APIView
import json
from django.http import Http404
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
from api.serializers import *
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes

@csrf_exempt
def login(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        email = data.get('email')
        password = data.get('password')

        
        
        try:
            #get user with associated email
            user = User.objects.get(email=email)
            matchcheck= check_password(password,user.password)
            print(user)
            if not matchcheck:
                #invalid password
                return JsonResponse({"message":"Invalid Password"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                token = Token.objects.get(user=user)
                context = {
                    'message' : "Login successful!",
                    'data' : {'token' : token.key}
                }
                return JsonResponse(context,safe=False, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            return JsonResponse({"message":"User not found"}, status=status.HTTP_204_NO_CONTENT)        
    else:
        return HttpResponse("Invalid method")

@csrf_exempt
def signup(request):

    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))

        # check if email exist
        if User.objects.filter(email=data.get('email')).exists():
            return JsonResponse({"message":"Email already exist"},safe=False, status=status.HTTP_409_CONFLICT)
        else:
            payload = {
                'email':data.get('email'),
                'username': data.get('email'),
                'last_name':data.get('last_name'),
                'first_name':data.get('first_name'),
                'password':data.get('password')
            }
    
            reg_serializer = RegisterSerializer(data=payload)
            if reg_serializer.is_valid():
                user = reg_serializer.create(payload)
                Token.objects.create(user=user)

                context = {
                        'message' : "Signup successful!",
                        'data' : {
                            'id' : user.getEncryptedID(),
                            'email': user.email,
                            'name': user.full_name()
                            }
                    }
                return JsonResponse(context,safe=False, status=status.HTTP_200_OK)
            else:
                return JsonResponse({"message":"Invalid"},safe=False, status=status.HTTP_409_CONFLICT)
    else:
        return HttpResponse("Invalid method")

class Blog(APIView):

    def get_object(self, pk):
        try:
            post = Post.objects.get(Q(pk=pk))
            return post
        except ObjectDoesNotExist:
            raise Http404

    # def get(self, request, pk, format=None):
    #     snippet = self.get_object(pk)
    #     serializer = PostSerializer(snippet)
    #     context = {
    #         'message' : "Success!",
    #         'data' : serializer.data
    #     }
    #     return JsonResponse(context,safe=False, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        payload = {
            'title' : request.data.get('title'),
            'content': request.data.get('content'),
            'posted_by': request.user.id,
        }
        serializer = PostSerializer(data=payload)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"message":"Post created!"},safe=False, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse({"message":"Error"},safe=False, status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        payload = {
            'title' : request.data.get('title'),
            'content': request.data.get('content'),
            'posted_by': request.user.id,
        }
        serializer = PostSerializer(snippet, payload)
        if serializer.is_valid():
            if snippet.posted_by == request.user:
                serializer.save()
                context = {
                    'message' : "Post updated!",
                    'data' : serializer.data
                }
                return JsonResponse(context,safe=False, status=status.HTTP_200_OK)
            else:
                return Response({"message":"Only the author can update this post"},status=status.HTTP_403_FORBIDDEN)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        if snippet.posted_by == request.user:
            snippet.delete()
            return Response({"message":"Remove"},status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message":"Only the author can delete this post"},status=status.HTTP_403_FORBIDDEN)


class BlogPublic(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get_object(self, pk):
        try:
            post = Post.objects.get(Q(pk=pk))
            return post
        except ObjectDoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = PostSerializer(snippet)
        context = {
            'message' : "Success!",
            'data' : serializer.data
        }
        return JsonResponse(context,safe=False, status=status.HTTP_200_OK)

class Blogs(ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    def get_queryset(self):
        posts = Post.objects.all().order_by('-id')
        return posts

class MyBlogs(ListAPIView):
    serializer_class = PostSerializer
    def get_queryset(self):
        posts = Post.objects.filter(posted_by=self.request.user).order_by('-id')
        return posts

class BlogComment(APIView):
    def get_object(self, pk):
        try:
            post = Post.objects.get(Q(pk=pk))
            return post
        except ObjectDoesNotExist:
            raise Http404

    #all comments in post
    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = CommentSerializer(snippet.post_comment.all(), many=True)
        context = {
            'message' : "Success!",
            'data' : serializer.data
        }
        return JsonResponse(context,safe=False, status=status.HTTP_200_OK)

    #delete comment
    def delete(self, request, pk, comment_pk,format=None):
        comment = Comment.objects.get(Q(pk=comment_pk))
        author = comment.post.posted_by
        if (comment.comment_by == request.user) or (author == request.user):
            comment.delete()
            return Response({"message":"Remove"},status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message":"Only the author can delete this post"},status=status.HTTP_403_FORBIDDEN)

    #create comment
    def post(self, request, pk,format=None):
        snippet = self.get_object(pk)
        payload = {
            'post': snippet.id,
            'content': request.data.get('content'),
            'comment_by': request.user.id,
        }
        serializer = CommentSerializer(data = payload)
        if serializer.is_valid():
            serializer.save()
            context = {
                'message' : "Comment created!",
                'data' : serializer.data
            }
            return JsonResponse(context,safe=False, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse({"message":"Error"},safe=False, status=status.HTTP_204_NO_CONTENT)