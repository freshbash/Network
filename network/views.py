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
from django.db import transaction

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
def formatPosts(user, dbposts):
    formattedPosts = []
    for post in dbposts:
        #Check if the post is already liked by the viewing user
        has_liked = checkLiked(user, post)
        #Check if the owner and viewer of the post are the same
        is_owner = user.username == post.user.username
        #Append the serialized post and has_liked state to the list as a dictionary.
        formattedPosts.append({"content": post.serialize(), "liked": has_liked, "is_owner": is_owner})
    
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
def index(request, pageNum=1):
    #Get the data for posts in page 1, Get the number of pages, Get the page number

    #Get all the posts from the db
    all_posts = list(Post.objects.all().order_by("-timestamp"))

    #Format the posts
    formattedPosts = formatPosts(request.user, all_posts)

    #Paginate the posts and get page 1
    num_pages, page = createPagination(formattedPosts, 10, pageNum)
    return render(request, "network/index.html", {
        "data": {"page": page, "num_pages": num_pages, "page_num": pageNum, "path": "/all", "user_logged_in": request.user.is_authenticated}
    })

#Function that redirects all request to "/all" to "/"
def redirect(request):
    return HttpResponseRedirect(reverse("index"))


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
    #Handle form submission
    if request.method == 'POST':
        content = request.POST['content']
        print("user", request.user)
        # Store post on the database
        post = Post(user=request.user, post=content)
        post.save()
        # Redirect to all posts.
        return HttpResponseRedirect(reverse('index'))
    
    #Render the create post page on a get request
    elif request.method == "GET":
        return render(request, 'network/createpost.html', status=200)


#Responds with the details of the requested user
@login_required
@csrf_exempt
def profile(request, usr_name, page_num=1):
    
    #Check if the user is viewing their own profile
    is_own_profile = False
    if request.user.username == usr_name:
        is_own_profile = True
    
    # get the details of the particular user.
    try:
        profileUser = User.objects.get(username=usr_name)
    except User.DoesNotExist:
        return HttpResponse(status=404)

    #Check if the viewer is following the profile or not, if the viewer and profile are not the same
    is_following = False
    try:
        if(Follower.objects.filter(user=profileUser, followed_by=request.user)):
            is_following = True
    except Follower.DoesNotExist:
        pass

    #Get the count of followers of that user
    followers = Follower.objects.filter(user=profileUser).count()

    #Get the count of users the user is following
    followings = Follower.objects.filter(followed_by=profileUser).count()

    #Create a connection count object
    connections = {
        "followers": followers,
        "followings": followings
    }

    #Get the posts of that user.
    user_posts = Post.objects.filter(user=profileUser).order_by('-timestamp').all()

    #Put the retrieved posts in an appropriate format
    user_posts = formatPosts(request.user, user_posts)

    #Create pagination object
    num_pages, page = createPagination(user_posts, 10, page_num)

    # pass it to the render function.
    return render(request, "network/profile.html", {
        "user_data": {"username": usr_name, "connections": connections, "bio": profileUser.bio, "is_own_profile": is_own_profile},
        "component_capsule": {"username": usr_name, "follower_count": connections["followers"], "is_following": is_following},
        "data": {"page": page, "num_pages": num_pages, "page_num": page_num, "path": "/user/"+usr_name, "user_logged_in": request.user.is_authenticated}
    }, status=200)


#Entertain requests to edit the user's profile
@login_required
def editProfile(request, username):
    #Get the user object
    user = User.objects.get(username=username)

    #Handle change to user profile
    if request.method == "POST" and request.user.username == username:
        #Get the data
        newUserName = request.POST["newUsername"]
        newBio = request.POST["newBio"]

        #Modify the user object with the new data
        user.username = newUserName
        user.bio = newBio

        #Save the changes
        user.save()

        #Redirect to profile page
        return HttpResponseRedirect(reverse("profile", kwargs={"usr_name": user.username}))

    #Render the profile change form
    elif request.method == "GET" and request.user.username == username:
        return render(request, "network/editProfile.html", {
            "userData": {"username": username, "userBio": user.bio}
        }, status=200)
    
    #Respond with a forbidden message
    else:
        return HttpResponse(status=403)


#API endpoint to handle follow/unfollow requests
@login_required
@csrf_exempt
def follow(request, usr):
    #Handle PUT requests
    if request.method == "PUT":
        try:
            user = User.objects.get(username=usr)
        except User.DoesNotExist:
            return HttpResponse(status=404)
        
        #Get the request body
        data = json.loads(request.body)

        #Check if it is a request to follow or unfollow
        if data.get("follow") == True:
            #Create a new follower
            follower = Follower(user=user, followed_by=request.user)
            follower.save()
        else:
            #Delete the follower
            Follower.objects.filter(user=user, followed_by=request.user).delete()

        #Return response with 204 status code
        return HttpResponse(status=204)
    else:
        return HttpResponse(status=403)


#Responds with the postings of the people the user follows
@login_required
def display_posts(request, pageNum=1):

    #Get the list of people the user follows
    followings_list = [person.user for person in Follower.objects.filter(followed_by=request.user)]
    
    #Empty array to be populated with posts of users in the above list
    posts = []

    #Get all the posts of the users in the list above, format them and add them to the posts array.
    for user in followings_list:
        user_posts = list(Post.objects.filter(user=user).order_by('-timestamp').all())
        formattedPosts = formatPosts(request.user, user_posts)
        posts.extend(formattedPosts)
    
    #Create a pagination object, get the first page and the number of pages
    pages, page = createPagination(posts, 10, pageNum)

    #Render template with the data
    return render(request, "network/following.html", {
        "data": {"page": page, "num_pages": pages, "page_num": pageNum, "path": "/following", "user_logged_in": request.user.is_authenticated}
    })


#Loads the appropriate page of posts
def load_nthpage(request, page_num, usn=None, path=None):

    #If path is not specified, then load the appropriate page of index
    if path == "all":
        return index(request, page_num)
    
    #If path is "following", then load the appropriate page of followings
    elif path == "following":
        return display_posts(request, page_num)
    #If path is "user", then load the appropriate page of user posts
    elif path == "user":
        return profile(request, usn, page_num)
       


#Entertains requests to make updates to a post's text content
@csrf_exempt
@login_required
def edit(request, post_id):

    #Handle PUT request
    if request.method == "PUT":

        #Get the concerned post object
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return HttpResponse("Error: Post does not exist anymore", status=401)
        
        #Convert the body from the request from json to a dictionary
        data = json.loads(request.body)

        #Get the updated post string
        newContent = data.get("content", post.post)

        #Modify the post object with the new post string
        post.post = newContent

        #Save the changes
        post.save()

        #return a successful response
        return JsonResponse({"post": post.post} ,status=200)
    
    return HttpResponse("Error: PUT request required", status=403)


#Function to entertain updates to the like count of a post
@csrf_exempt
@login_required
@transaction.atomic
def like(request, post_id):

    #Handle PUT request
    if request.method == 'PUT':

        #Convert the body of the request from json format
        data = json.loads(request.body)

        #Get the post in question
        post = Post.objects.get(pk=post_id)

        #Increment/decrement like count and Add/Delete a like object.
        if data.get("hasLiked") == True:
            post.likes = post.likes + 1
            Like(user_post=post, liked_by=request.user).save()
        else:
            post.likes = post.likes - 1
            Like.objects.filter(user_post=post, liked_by=request.user).delete()

        #Save the changes
        post.save()

        #Return the number of likes as a json response
        return JsonResponse({"likes": post.likes}, status=200)


    return HttpResponse("Error: PUT request required", status=403)
