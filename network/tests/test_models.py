from django.test import TestCase
from network.models import User, Post
import datetime

class TestModels(TestCase):

    def test_post_serialize(self):

        #Create a user
        test_user = User.objects.create(
            username="abc",
            email="a@b.com",
            password=123,
            bio="string"
        )

        #Create a post object for test user
        post = Post.objects.create(user=test_user, post="my post")

        #Get a serialized output
        output = post.serialize()

        #Check if the serialized output is in correct format

        #Check if the number of items in the serialized output is 5
        self.assertEquals(len(output), 5)

        #Check each element in the output

        #Check if id is an int
        self.assertEquals(output["id"], 1)
        self.assertEquals(type(output["id"]), int)

        #Check if the username is correct
        self.assertEquals(output["user"], "abc")

        #Check if the post is correct
        self.assertEquals(output["post"], "my post")

        #Check if like count is 0
        self.assertEquals(output["likes"], 0)

        #Check if the timestamp is valid
        self.assertEquals(type(output["timestamp"]), datetime.datetime)
