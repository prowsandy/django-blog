from django.urls import path
from api.views import *

urlpatterns = [
    path('auth/login', login, name='login'),
    path('auth/signup', signup, name='signup'),
    path('post', Blog.as_view()),
    path('post/<pk>', Blog.as_view()),
    path('me/posts', MyBlogs.as_view()),
    path('posts', Blogs.as_view()),
    path('posts/<pk>/comments', BlogComment.as_view()),
    path('posts/<pk>/comments/<comment_pk>', BlogComment.as_view())
]

