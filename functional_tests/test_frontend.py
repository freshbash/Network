import os
import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.common.by import By
from network.models import User, Post, Follower, Like

# Helpers

#Function to pause
def wait(n):
    time.sleep(n)

#Function to click an element with an id
def click(browser, id):
    browser.find_element(By.ID, id).click()

class TestNetworkWebsite(StaticLiveServerTestCase):

    #Set up code
    def setUp(self):
        #Set up chrome
        self.browser = webdriver.Chrome()
        
        #Create test users
        self.test_user_1  = User.objects.create(
            username="Neil",
            email="a@b.com",
            password=make_password("123"),
            bio="Neil's bio"
        )

        self.test_user_2  = User.objects.create(
            username="Mani",
            email="c@d.com",
            password=make_password("456"),
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
        wait(5)

        #Log test_user_1 in

        #Click on log in
        click(self.browser, "login")

        #Wait for 5 seconds
        wait(5)

        #Fill in the username
        self.browser.find_element(By.ID, "username").send_keys(self.test_user_1.username)

        #Fill in the password
        self.browser.find_element(By.ID, "password").send_keys("123")


        #Click the submit button
        click(self.browser, "submit")

        #Wait for 5 seconds
        wait(5)

        #Scroll to the bottom of the page
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        #Wait for 2 seconds
        wait(2)

        #Scroll to the top
        self.browser.execute_script("window.scrollTo(document.body.scrollHeight, 0);")

        #Wait for 5 seconds
        wait(5)

        #Click the create post link
        click(self.browser, "create")

        #Wait for 2 seconds
        wait(2)

        #Fill in the post content
        self.browser.find_element(By.ID, "post-content").send_keys("My first post")

        #Click the post button
        click(self.browser, "post-it")

        #Wait for 5 seconds
        wait(5)

        #Profile page section

        #Click on own profile
        click(self.browser, "profile")

        #Wait for 5 seconds
        wait(5)

        #Go to all posts page
        click(self.browser, "all-posts")

        #Click on someone else's profile
        collection = self.browser.find_element(By.ID, "all-posts-root")
        div = collection.find_element(By.XPATH, "./div")
        secondPostDiv = div.find_element(By.XPATH, "./div[2]")
        userBar = secondPostDiv.find_element(By.XPATH, "./div[1]")
        userNameDiv = userBar.find_element(By.ID, "user-name-post")
        userNameDiv.find_element(By.TAG_NAME, 'a').click()

        

        #Wait for 5 seconds
        wait(5)
