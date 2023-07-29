import os
import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import Client
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.common.by import By
from network.models import User, Post, Follower, Like

class TestNetworkWebsite(StaticLiveServerTestCase):

    def setUp(self):
        #Set up chrome
        self.browser = webdriver.Chrome()
        
        #Create test users
        self.test_user_1  = User.objects.create(
            username="abc",
            email="a@b.com",
            password="123",
            bio="test_user_1 bio"
        )

        self.test_user_2  = User.objects.create(
            username="def",
            email="c@d.com",
            password="456",
            bio="test_user_2 bio"
        )

        #Log test_user_1 in
        self.client.force_login(self.test_user_1)

        #Create 20 posts, 10 each for both users created
        for i in range(1, 11):
            Post.objects.create(user=self.test_user_1, post="Post number: "+str(i)+" by user: "+self.test_user_1.username)
        for i in range(11, 21):
            Post.objects.create(user=self.test_user_2, post="Post number: "+str(i)+" by user: "+self.test_user_2.username)

    def tearDown(self):
        self.browser.close()

    def test_all_posts_page(self):
        
        #Make a get request to the appropriate page
        self.browser.get(self.live_server_url)

        #Wait for 5 seconds
        time.sleep(5)

        #Click the  all posts link
        self.browser.find_element(By.ID, "all-posts")

        #Scroll to the bottom of the page
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        #Wait for 2 seconds
        time.sleep(2)

        #Scroll to the top
        self.browser.execute_script("window.scrollTo(document.body.scrollHeight, 0);")

        #Wait for 5 seconds
        time.sleep(5)
