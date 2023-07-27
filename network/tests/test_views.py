from django.test import TestCase, Client
from django.urls import reverse
from network.models import User, Follower, Post, Like
import json

class TestViews(TestCase):

    #Define setup
    def setUp(self):
        self.client = Client()
        #Create a user
        self.username1="abc"
        self.password1=123
        self.username2="def"
        self.password2="456"

        self.test_user = User.objects.create(
            username=self.username1,
            email="a@b.com",
            password=self.password1,
            bio="stirng"
        )

        self.test_user_2 = User.objects.create(
            username=self.username2,
            email="c@d.com",
            password=self.password2,
            bio="string"
        )

    #Check index view
    def test_index_GET(self):
        
        #Get response to a get request
        response = self.client.get(reverse("index"))

        #Check that the response status code is 200 and that the correct template is rendered
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "network/index.html")
    
    #Check is "redirect" function redirects correctly
    def test_redirect(self):

        #Get response to a get request
        response = self.client.get(reverse("index_p"))

        #Check that response status code is 302
        self.assertEquals(response.status_code, 302)

    #Check if "createpost.html" is getting rendered on sending a get request
    def test_create_GET(self):

        #Get response
        response = self.client.get(reverse("create"))

        #Check whether status code is 302
        self.assertEquals(response.status_code, 302)

    #Check post creation
    def test_create_POST(self):
        
        #Log the user in
        self.client.force_login(self.test_user)

        #Get a response from the post request to "create"
        response = self.client.post(reverse("create"), {
            "content": "9f8sahf"
        })

        #Check the response code
        self.assertEquals(response.status_code, 302)
        #Check if the post is added
        self.assertEquals(Post.objects.all().count(), 1)

    #Test whether profile view is working correctly
    def test_profile(self):

        #Log the dummy user in
        self.client.force_login(self.test_user)

        #Make a GET request to get the profile view of our dummy user
        response = self.client.get(reverse("profile", args=[self.test_user.username]))

        #Check whether the response code is 200
        self.assertEquals(response.status_code, 200)

    #Check GET request to editProfile view
    def test_editProfile_GET(self):

        #Log test_user in
        self.client.force_login(self.test_user)

        #Make a GET request from test_user to get the edit profile form for test_user
        response1 = self.client.get(reverse("edit_profile", args=[self.test_user.username]))

        #Check if response1 returns 200 as status code
        self.assertEquals(response1.status_code, 200)

        #Make a GET request from test_user to get the edit profile of test_user_2
        response2 = self.client.get(reverse("edit_profile", args=[self.test_user_2.username]))

        #Check if response2 returns 403 as status code
        self.assertEquals(response2.status_code, 403)

    def test_editProfile_POST(self):

        #Log test_user in
        self.client.force_login(self.test_user)

        #Make a POST request from test_user to update the profile of test_user
        response1 = self.client.post(reverse("edit_profile", args=[self.test_user.username]), {
            "newUsername": "acb",
            "newBio": "String"
        })

        #Check if response1 returns 302 as status code
        self.assertEquals(response1.status_code, 302)

        #Check if the updation was complete
        self.assertEquals(User.objects.filter(username="acb", bio="String").all().count(), 1)

        #Make a POST request from test_user to update the profile of test_user_2
        response2 = self.client.get(reverse("edit_profile", args=[self.test_user_2.username]), {
            "newUsername": "efd",
            "newBio": "Sting"
        })

        #Check if response2 returns 403 as status code
        self.assertEquals(response2.status_code, 403)


    #Check if the "Following view" is working correctly
    def test_following(self):

        #Log the user in
        self.client.force_login(self.test_user)

        #Make a GET request
        response = self.client.get(reverse("following"))

        #Check if the status code in the response is 200
        self.assertEquals(response.status_code, 200)

    
    #Check the all brach of the view to display different pages of posts
    def test_loadnthpage_all(self):

        #Create 20 posts for test_user
        for i in range(1, 21):
            Post.objects.create(user=self.test_user, post=str(i))

        #Make a GET request to get page 2 of index
        response = self.client.get(reverse("following_p", kwargs={"path": "all", "page_num": 2}))

        #Check if the returned response is 200
        self.assertEquals(response.status_code, 200)

    
    #Check the following branch of load_nthpage view
    def test_loadnthpage_following(self):

        #Make test_user follow test_user_2
        Follower.objects.create(user=self.test_user_2, followed_by=self.test_user)

        #Create 20 posts for test_user_2
        for i in range(1, 21):
            Post.objects.create(user=self.test_user_2, post=str(i))

        #Log test_user in
        self.client.force_login(self.test_user)

        #Make a GET request to go to the 2nd page of the following tab of test_user
        response = self.client.get(reverse("following_p", kwargs={"path":"following", "page_num": 2}))

        #Check if the response status code is 200
        self.assertEquals(response.status_code, 200)
    
    #Check the "user" branch of load_nthpage view
    def test_loadnthpage_user(self):

        #Check for the posts of the logged in user

        #Create 20 posts for test_user
        for i in range(1, 21):
            Post.objects.create(user=self.test_user, post=str(i))

        #Log test_user in
        self.client.force_login(self.test_user)

        #Make a GET request to get page 2 of posts at test_user's profile page
        response = self.client.get(reverse("profile_p", kwargs={"path":"user", "usn":self.test_user.username, "page_num":2}))

        #Check if the response status code is 200
        self.assertEquals(response.status_code, 200)

        #Check for the posts of another user

        #Create 20 posts for test_user_2
        for i in range(1, 21):
            Post.objects.create(user=self.test_user_2, post=str(i))

        #Make a GET request to get page 2 of posts created by test_user_2
        response2 = self.client.get(reverse("profile_p", kwargs={"path":"user", "usn":self.test_user_2.username, "page_num":2}))

        #Check if the response status code is 200
        self.assertEquals(response.status_code, 200)
