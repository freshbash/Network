#Import dependencies
from network.models import Like
from django.core.paginator import Paginator


#Helper functions for views


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


#Function to create a Pagination object and return the number of pages and contents for page 1.
def createPagination(posts, posts_per_page, page_num):
    #Create a pagination object
    p = Paginator(posts, posts_per_page)

    #Get the contents of the required page
    page = list(p.page(page_num).object_list)

    #Return the number of pages and first page content
    return p.num_pages, page
