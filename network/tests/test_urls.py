from django.test import TestCase
from django.urls import reverse, resolve
from network.views import index, create, profile, editProfile, display_posts, redirect, load_nthpage, follow, edit, like

# Create your tests here.

class TestUrls(TestCase):

    #Test the index route
    def test_index_url(self):
        
        #Get the url
        url = reverse("index")

        #Compare the resolved function with the intended view
        self.assertEquals(resolve(url).func, index)

    #Test the create post route
    def test_create(self):

        #Get the url
        url = reverse("create")

        #Compare the resolved function with the intended view
        self.assertEquals(resolve(url).func, create)

    #Test the profile view route
    def test_profile(self):

        #Get the url
        url = reverse("profile", args=["usr_name"])

        #Compare the resolved function with the intended view
        self.assertEquals(resolve(url).func, profile)

    #Test the edit profile route
    def test_edit_profile(self):

        #Get the url
        url = reverse("edit_profile", args=["username"])

        #Compare the resolved function with the intended view
        self.assertEquals(resolve(url).func, editProfile)

    #Test following route
    def test_following(self):

        #Get the url
        url = reverse("following")

        #Compare the resolved function with the intended view
        self.assertEquals(resolve(url).func, display_posts)

    #Test all route
    def test_all(self):

        #Get the url
        url = reverse("index_p")

        #Compare the resolved function with the intended view
        self.assertEquals(resolve(url).func, redirect)

    #Test pagination route for following
    def test_pagination_following(self):

        #Get the url
        url = reverse("following_p", kwargs={"path": "following", "page_num": 2})

        #Compare the resolved function with the intended view
        self.assertEquals(resolve(url).func, load_nthpage)

    #Test pagination route for profile
    def test_pagination_profile(self):

        #Get the url
        url = reverse("profile_p", kwargs={"path": "user", "usn": "some_person", "page_num": 2})

        #Compare the resolved function with the intended view
        self.assertEquals(resolve(url).func, load_nthpage)

    #Test api route for follow/unfollow request
    def test_follow(self):

        #Get the url
        url = reverse("follow", args=["usr"])

        #Compare the resolved function with the intended view
        self.assertEquals(resolve(url).func, follow)

    #Test api route for edit post requests
    def test_edit(self):

        #Get the url
        url = reverse("edit", args=[1])

        #Compare the resolved function with the intended view
        self.assertEquals(resolve(url).func, edit)

    #Test api route for like/unlike requests
    def test_like(self):

        #Get the url
        url = reverse("like", args=[1])

        #Compare the resolved function with the intended view
        self.assertEquals(resolve(url).func, like)


