import os
import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import Client
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.common.by import By
from network.models import User, Post, Follower, Like

class TestNetworkWebsite(StaticLiveServerTestCase):

    #Set up code
    def setUp(self):
        #Set up chrome
        self.browser = webdriver.Chrome()

        self.client = Client()
        
        #Create test users
        self.test_user_1  = User.objects.create(
            username="Neil",
            email="a@b.com",
            password=123,
            bio="Neil's bio"
        )

        self.test_user_2  = User.objects.create(
            username="Mani",
            email="c@d.com",
            password=456,
            bio="Mani's bio"
        )

        #Create 20 posts, 10 each for both users created
        for i in range(1, 11):
            Post.objects.create(user=self.test_user_1, post="Post number: "+str(i)+" by user: "+self.test_user_1.username)
        for i in range(11, 21):
            Post.objects.create(user=self.test_user_2, post="Post number: "+str(i)+" by user: "+self.test_user_2.username)

        #Make a get request to the appropriate page
        self.browser.get(self.live_server_url)


    #Close the browser
    def tearDown(self):
        self.browser.close()


    #Test the web app
    def test_all_posts_page(self):

        #Wait for 5 seconds
        time.sleep(2)

        #Log test_user_1 in

        #Click on log in
        self.browser.find_element(By.ID, "register").click()

        #Wait for 5 seconds
        time.sleep(2)

        #Fill in the username
        self.browser.find_element(By.ID, "username").send_keys("Venugopal")

        #Fill in the email
        self.browser.find_element(By.ID, "email").send_keys("e@f.com")

        #Fill in the bio
        self.browser.find_element(By.ID, "about").send_keys("Venugopal's bio")

        #Fill in the password
        self.browser.find_element(By.ID, "password").send_keys(789)

        #Fill in the confirmation
        self.browser.find_element(By.ID, "confirmation").send_keys(789)

        #Click the submit button
        self.browser.find_element(By.ID, "register-user").click()

        #Wait for 5 seconds
        time.sleep(2)

        #Scroll to the bottom of the page
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        #Wait for 2 seconds
        time.sleep(2)

        #Scroll to the top
        self.browser.execute_script("window.scrollTo(document.body.scrollHeight, 0);")

        #Wait for 5 seconds
        time.sleep(2)

        #Click the create post link
        self.browser.find_element(By.ID, "create").click()

        #Wait for 2 seconds
        time.sleep(2)

        #Fill in the post content
        self.browser.find_element(By.ID, "post-content").send_keys("My first post")

        #Click the post button
        self.browser.find_element(By.ID, "post-it").click()

        #Wait for 5 seconds
        time.sleep(5)
