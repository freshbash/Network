from django.test import TestCase, Client
from django.urls import reverse
from network.models import User, Follower, Post, Like
import json

class TestViews(TestCase):

    #Define setup
    def setUp(self):
        self.client = Client()
        #Create a user
        self.username="abc",
        self.password=123,
        self.test_user = User.objects.create(
            username=self.username,
            email="a@b.com",
            password=self.password,
            bio="stirng"
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

        #Check whether status code is 200 OK
        self.assertEquals(response.status_code, 302)

    #Check post creation
    def test_create_POST(self):

        self.client.force_login(self.test_user)

        response = self.client.post(reverse("create"), {
            "content": "9f8sahf"
        })

        #Check the response code
        self.assertEquals(response.status_code, 302)
        #Check if the post is added
        self.assertEquals(Post.objects.all().count(), 1)
