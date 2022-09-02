import json
from os import stat
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .models import Posts, User, Followers, Followings, Likes


def index(request):
    # Get all the posts from the database.
    post_details = []
    all_posts = list(Posts.objects.all().order_by("-datetime"))
    for post in all_posts:
        has_liked = False
        try:
            if(Likes.objects.filter(user_post=post, like=request.user.id)):
                has_liked = True
        except Likes.DoesNotExist:
            pass
        post_detail = {"post": post, "liked": has_liked}
        post_details.append(post_detail)
    p = Paginator(post_details, 10)
    num_pages = [num for num in range(1, p.num_pages + 1)]
    page1 = list(p.page(1).object_list)
    return render(request, "network/index.html", {
        "num_pages": num_pages, "page": page1
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        bio = request.POST["about"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password, bio=bio)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required
@csrf_exempt
def create(request):
    if request.method == 'POST':
        content = request.POST['content']
        # Store post on the database
        post = Posts(user=request.user, post=content)
        post.save()
        # Redirect to all posts.
        return HttpResponseRedirect(reverse('index'))
    return render(request, 'network/createpost.html')

@login_required
@csrf_exempt
def profile(request, usr_name):
    # get the details of the particular user.
    try:
        user = User.objects.get(username=usr_name)
    except User.DoesNotExist:
        return HttpResponse(status=404)

    #Get the connections of that user.
    is_following = False
    try:
        if(Followers.objects.filter(user=user, followers=request.user)):
            is_following = True
    except Followers.DoesNotExist:
        pass
    followers = len(list(Followers.objects.filter(user=user)))
    followings = len(list(Followings.objects.filter(user=user)))
    connections = {
        "followers": followers,
        "followings": followings
    }

    # get the post of that user.
    user_posts = Posts.objects.filter(user=user).order_by('-datetime').all()
    user_details = []
    for post in user_posts:
        has_liked = False
        try:
            if (Likes.objects.filter(user_post=post, like=request.user.id)):
                has_liked = True
        except Likes.DoesNotExist:
            pass
        user_detail = {"post": post, "liked": has_liked}
        user_details.append(user_detail)
    p = Paginator(user_details, 10)
    num_pages = [num for num in range(1, p.num_pages + 1)]
    page = p.page(1).object_list
    # pass it to the render function.
    return render(request, "network/profile.html", {
        "user_data": user, "page": page, "is_following": is_following,
        "connections": connections, "num_pages": num_pages
    })

@login_required
@csrf_exempt
def follow(request, usr):

    try:
        user = User.objects.get(username=usr)
    except User.DoesNotExist:
        return HttpResponse(status=404)
    
    data = json.loads(request.body)
    if data["followers"] == True:
        follower = Followers(user=user, followers=request.user)
        follower.save()
        following = Followings(user=request.user, followings=user)
        following.save()
    elif data["followers"] == False:
        Followers.objects.filter(user=user, followers=request.user).delete()
        Followings.objects.filter(user=request.user, followings=user).delete()


    return HttpResponse(status=204) 

@login_required
def display_posts(request):
    followings_list = [following.followings for following in Followings.objects.filter(user=request.user)]
    
    posts = []

    for user in followings_list:
        user_posts = list(Posts.objects.filter(user=user).order_by('-datetime').all())
        for post in user_posts:
            has_liked = False
            try:
                if(Likes.objects.filter(user_post=post, like=request.user)):
                    has_liked = True
            except Likes.DoesNotExist:
                pass
            post_details = {"post": post, "liked": has_liked}
            posts.append(post_details)

    p = Paginator(posts, 10)

    num_pages = [num for num in range(1, p.num_pages + 1)]

    page = p.page(1).object_list


    return render(request, "network/following.html", {
        "page": page, "num_pages": num_pages
    })

def load_nthpage(request, page_num, path=None):
    if path == "all":
        if page_num == 1:
            return HttpResponseRedirect(reverse("index"))
        post_details = []
        all_posts = list(Posts.objects.all().order_by("-datetime"))
        for post in all_posts:
            has_liked = False
            try:
                if(Likes.objects.filter(user_post=post, like=request.user)):
                    has_liked = True
            except Likes.DoesNotExist:
                pass
            post_detail = {"post": post, "liked": has_liked}
            post_details.append(post_detail)
        p = Paginator(post_details, 10)
        num_pages = [num for num in range(1, p.num_pages + 1)]
        page = p.page(page_num).object_list
        return render(request, "network/index.html", {
            "num_pages": num_pages, "page": page
        })
    elif path == "following":
        if page_num == 1:
            return HttpResponseRedirect(reverse("following"))

        followings_list = [following.followings for following in Followings.objects.filter(user=request.user)]
    
        posts = []

        for user in followings_list:
            user_posts = list(Posts.objects.filter(user=user).order_by('-datetime').all())
            for post in user_posts:
                has_liked = False
                try:
                    if(Likes.objects.filter(user_post=post, like=request.user)):
                        has_liked = True
                except Likes.DoesNotExist:
                    pass
                post_details = {"post": post, "liked": has_liked}
                posts.append(post_details)

        p = Paginator(posts, 10)

        num_pages = [num for num in range(1, p.num_pages + 1)]

        page = p.page(page_num).object_list


        return render(request, "network/following.html", {
            "page": page, "num_pages": num_pages
        })
    elif path == "profile":
        if page_num == 1:
           return HttpResponseRedirect(f"/user/{request.user.username}")
        # get the details of the particular user.
        try:
            user = User.objects.get(username=request.user.username)
        except User.DoesNotExist:
            return HttpResponse(status=404)

        #Get the connections of that user.
        is_following = False
        try:
            if(Followers.objects.filter(user=user, followers=request.user)):
                is_following = True
        except Followers.DoesNotExist:
            pass
        followers = len(list(Followers.objects.filter(user=user)))
        followings = len(list(Followings.objects.filter(user=user)))
        connections = {
            "followers": followers,
            "followings": followings
        }

        # get the post of that user.
        user_posts = Posts.objects.filter(user=user).order_by('-datetime').all()
        user_details = []
        for post in user_posts:
            has_liked = False
            try:
                if(Likes.object.filter(user_post=post, like=request.user.id)):
                    has_liked = True
            except Likes.DoesNotExist:
                pass
            
            user_detail = {"post": post, "liked": has_liked}
            user_details.append(user_detail)
        p = Paginator(user_details, 10)
        num_pages = [num for num in range(1, p.num_pages + 1)]
        page = p.page(page_num).object_list
        # pass it to the render function.
        return render(request, "network/profile.html", {
            "user_data": user, "page": page, "is_following": is_following,
            "connections": connections, "num_pages": num_pages
        })         

@csrf_exempt
@login_required
def edit(request, post_id):
    # Get the post details

    if request.method == 'POST':
        post = Posts.objects.get(pk=post_id)
        
        data = json.loads(request.body)

        edited = data["post"]

        post.post = edited

        post.save()

        return JsonResponse({"post": post.post}, safe=False ,status=204)
    
    return HttpResponse("Error: Post request required", status=403)

@csrf_exempt
@login_required
def like(request, post_id):
    if request.method == 'PUT':
        data = json.loads(request.body)

        post = Posts.objects.get(pk=post_id)

        if data["increment"] == True:
            post.likes += 1
            liked = Likes(user_post=post, like=request.user)
            liked.save()
        elif data["increment"] == False:
            post.likes -= 1
            Likes.objects.filter(user_post=post, like=request.user).delete()
        post.save()

        likes = post.likes

        return JsonResponse({"likes": likes}, status=204)


    return HttpResponse("Error: PUT request required", status=403)
