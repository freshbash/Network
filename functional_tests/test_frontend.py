import os
import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium import webdriver

class TestNetworkWebsite(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.close()

    def test_all_posts_page(self):
        
        #Make a get request to the appropriate page
        self.browser.get(self.live_server_url)
        time.sleep(60)
        self.assertEquals(self.browser.title, "Social Network")