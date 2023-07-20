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

from .models import Post, User, Follower, Like


#=========================================================================================================================================
#Helper functions

#Check if the post is liked by the viewing user.
def checkLiked(user, post):
    has_liked = False
    #If the user has liked the post then set has_liked to true
    try:
        if(Like.objects.filter(user_post=post, liked_by=user.id)):
            has_liked = True
    except Like.DoesNotExist:
        pass
    return has_liked

#-----------------------------------------------------------------------------------------------------------------------------------------

#Function to take in data retrived from the db and the user object and return a list of formatted posts.
def formatPosts(user, posts):
    formattedPosts = []
    for post in posts:
        #Check if the post is already liked by the viewing user
        has_liked = checkLiked(user, post)
        #Append the serialized post and has_liked state to the list as a dictionary.
        formattedPosts.append({"content": post.serialize(), "liked": has_liked})
    
    return formattedPosts

#-----------------------------------------------------------------------------------------------------------------------------------------

#Function to create a Pagination object and return the number of pages and contents for page 1.
def createPagination(posts, posts_per_page, page_num):
    #Create a pagination object
    p = Paginator(posts, posts_per_page)

    #Get the contents of the required page
    page = list(p.page(page_num).object_list)

    #Return the number of pages and first page content
    return p.num_pages, page
#=========================================================================================================================================


#Responds with page 1 of all the posts
def index(request):
    #Get the data for posts in page 1, Get the number of pages, Get the page number

    #Get all the posts from the db
    all_posts = list(Post.objects.all().order_by("-timestamp"))

    #Format the posts
    formattedPosts = formatPosts(request.user, all_posts)

    #Paginate the posts and get page 1
    num_pages, page = createPagination(formattedPosts, 10, 1)
    return render(request, "network/index.html", {
        "data": {"page": page, "num_pages": num_pages, "page_num": 1}
    })


#Logs the user in and redirects to the index page
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


#Logs the user out
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))



#Registers a new user
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



#Accepts a post request to create and store a new posting.
@login_required
# @csrf_exempt
def create(request):
    if request.method == 'POST':
        content = request.POST['content']
        # Store post on the database
        post = Post(user=request.user, post=content)
        post.save()
        # Redirect to all posts.
        return HttpResponseRedirect(reverse('index'))
    
    #Render the create post page on a get request
    elif request.method == "GET":
        return render(request, 'network/createpost.html')


#Responds with the details of the requested user
@login_required
@csrf_exempt
def profile(request, usr_name):

    # get the details of the particular user.
    try:
        profileUser = User.objects.get(username=usr_name)
    except User.DoesNotExist:
        return HttpResponse(status=404)

    #Get the connections of that user.
    is_following = False
    try:
        if(Follower.objects.filter(user=profileUser, followed_by=request.user)):
            is_following = True
    except Follower.DoesNotExist:
        pass
    followers = Follower.objects.filter(user=profileUser).count()
    followings = Follower.objects.filter(followed_by=profileUser).count()
    connections = {
        "followers": followers,
        "followings": followings
    }

    #Get the posts of that user.
    user_posts = Post.objects.filter(user=profileUser).order_by('-datetime').all()

    #Use the retrieved posts to determine which of the posts the viewer has liked. 
    user_posts = formatPosts(request.user, user_posts)

    #Create pagination
    num_pages, page = createPagination(user_posts, 10)

    # pass it to the render function.
    return render(request, "network/profile.html", {
        "user_data": profileUser, "page": page, "is_following": is_following,
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
        follower = Follower(user=user, followers=request.user)
        follower.save()
        # following = Following(user=request.user, followings=user)
        # following.save()
    elif data["followers"] == False:
        Follower.objects.filter(user=user, followers=request.user).delete()
        # Following.objects.filter(user=request.user, followings=user).delete()


    return HttpResponse(status=204) 


#Responds with the postings of the people the user follows
@login_required
def display_posts(request):

    #Get the list of people the user follows
    followings_list = [person.user for person in Follower.objects.filter(followed_by=request.user)]
    
    posts = []

    for user in followings_list:
        user_posts = list(Post.objects.filter(user=user).order_by('-datetime').all())
        for post in user_posts:
            has_liked = False
            try:
                if(Like.objects.filter(user_post=post, liked_by=request.user)):
                    has_liked = True
            except Like.DoesNotExist:
                pass
            post_details = {"post": post, "liked": has_liked}
            posts.append(post_details)

    p = Paginator(posts, 10)

    num_pages = [num for num in range(1, p.num_pages + 1)]

    page = p.page(1).object_list


    return render(request, "network/following.html", {
        "page": page, "num_pages": num_pages
    })


#Woefully inefficient and violating!!!
def load_nthpage(request, page_num, path=None):
    if path == "all":
        if page_num == 1:
            return HttpResponseRedirect(reverse("index"))
        post_details = []
        all_posts = list(Post.objects.all().order_by("-datetime"))
        for post in all_posts:
            has_liked = False
            try:
                if(Like.objects.filter(user_post=post, liked_by=request.user)):
                    has_liked = True
            except Like.DoesNotExist:
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

        # followings_list = [following.followings for following in Following.objects.filter(user=request.user)]
    
        posts = []

        # for user in followings_list:
        #     user_posts = list(Post.objects.filter(user=user).order_by('-datetime').all())
        #     for post in user_posts:
        #         has_liked = False
        #         try:
        #             if(Like.objects.filter(user_post=post, liked_by=request.user)):
        #                 has_liked = True
        #         except Like.DoesNotExist:
        #             pass
        #         post_details = {"post": post, "liked": has_liked}
        #         posts.append(post_details)

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
            if(Follower.objects.filter(user=user, followers=request.user)):
                is_following = True
        except Follower.DoesNotExist:
            pass
        followers = len(list(Follower.objects.filter(user=user)))
        # followings = len(list(Following.objects.filter(user=user)))
        connections = {
            "followers": followers,
            # "followings": followings
        }

        # get the post of that user.
        user_posts = Post.objects.filter(user=user).order_by('-datetime').all()
        user_details = []
        for post in user_posts:
            has_liked = False
            try:
                if(Like.object.filter(user_post=post, liked_by=request.user.id)):
                    has_liked = True
            except Like.DoesNotExist:
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
        post = Post.objects.get(pk=post_id)
        
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

        post = Post.objects.get(pk=post_id)

        if data["increment"] == True:
            post.likes += 1
            liked = Like(user_post=post, like=request.user)
            liked.save()
        elif data["increment"] == False:
            post.likes -= 1
            Like.objects.filter(user_post=post, like=request.user).delete()
        post.save()

        likes = post.likes

        return JsonResponse({"likes": likes}, status=204)


    return HttpResponse("Error: PUT request required", status=403)
