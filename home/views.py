from django.shortcuts import render, HttpResponse
from home.models import *
from rest_framework.authtoken.models import Token

def index(request):
    return HttpResponse("Home")


def seed(request):
    #create 1 user
    user = User.objects.create(
        username = "userone",
        email = "john@email.com",
        first_name = "John",
        last_name = "Doe"
    )
    user.set_password("john001")
    user.save()
    Token.objects.create(user=user)

    #create post 1
    post1 = Post.objects.create(
        title = "What is Django",
        content = "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        posted_by = user
    )

    #create post 2
    post2 = Post.objects.create(
        title = "How to Django",
        content = "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        posted_by = user
    )


    #comments post 1
    for i in range(2):
        Comment.objects.create(
            post = post1,
            content = "Post 1 comment {}".format(i),
            comment_by = user
        )

    #comments post 2
    for i in range(2):
        Comment.objects.create(
            post = post2,
            content = "Post 2 comment {}".format(i),
            comment_by = user
        )

    return HttpResponse("Seeding complete")
