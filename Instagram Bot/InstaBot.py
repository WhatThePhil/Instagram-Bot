from data import Data
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from random import randint
import time, re, requests, sys

class Instagram():

    #takes care of emojis... .translate(non_bmp_map)

    def __init__(self, data, driver):
            self.username = data.get_username()
            self.password = data.get_pw()
            self.driver = driver
            self.data = data
            self.non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

    def login(self):
        self.driver.get('https://www.instagram.com/accounts/login/')
        self.driver.implicitly_wait(10)

        #input username and pw
        user = self.driver.find_element_by_xpath("//input[@name='username']")
        user.send_keys(self.username)

        pw = self.driver.find_element_by_xpath("//input[@name='password']")
        pw.send_keys(self.password)

        #locate and click on button
        loginBtn = self.driver.find_element_by_xpath("//button[contains(text(),'Log in')]")
        loginBtn.click()

    def gather_hashtag(self, hashtag, n):
        try:
            if("#" in hashtag):
                temp = hashtag[1:]
                hashtag = temp
                
            self.driver.get("https://www.instagram.com/explore/tags/" + hashtag)
            self.driver.implicitly_wait(1)

            total = int(n)
            loop = int(total/5)

            try:
                load = self.driver.find_element_by_xpath("//a[contains(text(),'Load more')]")
                time.sleep(0.5)
                load.click()

                for _ in range(loop):
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(0.2)
                    self.driver.execute_script("return document.body.scrollHeight")

                posts_raw = self.driver.find_elements_by_tag_name("a")

                for i in range(len(posts_raw)):
                    temp = posts_raw[i].get_attribute("href")
                    if(("/?tagged=" + hashtag) in temp):
                        if(self.data.get_total() < total+6):
                            self.data.add_users(temp)

                for i in range(9):
                    self.data.remove_begin_elem()
                    
                self.data.make_set()
            except Exception:
                return
            

        except Exception as e:
            print(e)
            
    def gather_commentors(self, post, n):
        #initial comments loaded are 20
        #first expand seems random 20+
        #loading more is 20+ as well
        try:
            if("https://www.instagram.com/" in post):
                self.driver.get(post)
                self.driver.implicitly_wait(1)
            else:
                self.driver.get("https://www.instagram.com/" + post)
                self.driver.implicitly_wait(1)
        except Exception:
            return

        try:
            self.driver.find_element_by_xpath("//h2[contains(text(),'Sorry, this page isn't available.')]")
            return
        except Exception:
            total = int(n)
            loop = int(total/20)

        try:
            #11 loops is about 250+ usernames
            expand_comments = self.driver.find_element_by_xpath("//button[contains(text(),'view all')]")
            expand_comments.click()
            time.sleep(0.5)

            for _ in range(loop):
                loadmore_comments = self.driver.find_element_by_xpath("//button[contains(text(),'load more comments')]")
                loadmore_comments.click()
                time.sleep(0.25)
                
        except Exception as e:
           None

        try:
            #comments are loaded. we can gather all usernames
            users_raw = self.driver.find_elements_by_tag_name("a")
            for i in range(len(users_raw)):
                if(users_raw[i].get_attribute("title") != ""):
                    if(self.data.get_total() < total+2):
                        self.data.add_users(users_raw[i].get_attribute("title"))

            #removes repeated username
            self.data.remove_begin_elem()
            self.data.remove_begin_elem()
            self.data.make_set()
        except Exception:
            return

    def gather_f(self, user, n, f):
        try:
            total = int(n)
            loops = int(total/3)
            
            if(len(user) < 30):
                self.driver.get("https://www.instagram.com/" + user)
            else:
                self.driver.get(user)
                
            self.driver.implicitly_wait(1)

            if(f == "following"):
                btn = self.driver.find_element_by_xpath("//a[contains(text(),'following')]")
            else:
                btn = self.driver.find_element_by_xpath("//a[contains(text(),'followers')]")
                
            btn.click()
            time.sleep(1)
            
            load = self.driver.find_elements_by_tag_name("li")

            for _ in range(loops):
                load[len(load)-1].location_once_scrolled_into_view
                load = self.driver.find_elements_by_xpath("//button[contains(text(),'Follow')]")
                self.driver.implicitly_wait(2)
                

            users_raw = self.driver.find_elements_by_tag_name("a")
            for i in range(len(users_raw)):
                if(users_raw[i].get_attribute("title") != ""):
                    if(self.data.get_total() < total):
                        self.data.add_users(users_raw[i].get_attribute("title"))

            self.data.make_set()
        except Exception:
            return


    def follow(self, username, dont_follow_private):
        try:
            user = username
            if("https://www.instagram.com/" in user):
                self.driver.get(user)
            else:
                self.driver.get("https://www.instagram.com/" + user)
                
            self.driver.implicitly_wait(1)
            time.sleep(3)

            try:
                self.driver.find_element_by_xpath("//h2[contains(text(),'No posts yet.')]")
                return True
            except Exception:
                if(dont_follow_private == 1):
                    try:
                        self.driver.find_element_by_xpath("//h2[contains(text(),'This Account is Private')]")
                        return True
                    except Exception:
                        followBtn = self.driver.find_element_by_xpath("//button[contains(text(),'Follow')]")
                        followBtn.click()
                        return False
                else:
                    followBtn = self.driver.find_element_by_xpath("//button[contains(text(),'Follow')]")
                    followBtn.click()
                    return False
        except Exception as e:
            return True

    def unfollow(self):
        username = self.data.get_username()
        self.driver.get("https://www.instagram.com/" + username)
        self.driver.implicitly_wait(2)

        following = self.driver.find_element_by_xpath("//a[contains(text(),'following')]")
        time.sleep(randint(1, 3))
        following.click()
        time.sleep(randint(1, 3))

        for _ in range(randint(1, 8)):
            time.sleep(randint(1, 3))
            unfollowBtn = self.driver.find_element_by_xpath("//button[contains(text(),'Following')]")
            time.sleep(randint(1, 3))
            unfollowBtn.click()
            self.data.update_unfollow_total()

    def comment_like(self, comment_bool, like_bool, comment_text, username):
        user = username
        posts = []

        if("https://www.instagram.com/" in user):
            self.driver.get(user)
        else:
            self.driver.get("https://www.instagram.com/" + user)
            
        self.driver.implicitly_wait(1)
        time.sleep(2)
            
        try:
            self.driver.find_element_by_xpath("//h2[contains(text(),'This Account is Private')]")
            return True
            
        except Exception:
            try:
                self.driver.find_element_by_xpath("//h2[contains(text(),'No posts yet.')]")
                return True
                
            except Exception:
                if("https://www.instagram.com/" not in user):
                    posts_raw = self.driver.find_elements_by_tag_name("a")
                    posts_raw.pop(0)
                    posts_raw.pop(0)

                    for i in range(len(posts_raw)):
                        temp = posts_raw[i].get_attribute("href")
                        if( ("/?taken-by=" + user) in temp):
                            posts.append(temp)

                    if(len(posts) > 2):
                        self.driver.get(posts[randint(0, 2)])
                    else:
                        try:
                            self.driver.get(posts[0])
                        except Exception:
                            return True
                        
                    self.driver.implicitly_wait(1)
                    time.sleep(2)

                else:
                    try:
                        if(like_bool):
                            try:
                                likeBtn = self.driver.find_element_by_xpath("//span[contains(text(),'Like')]")
                                likeBtn.click()
                            except Exception:
                                print("Already Liked Post")
                            time.sleep(2)
                            return False

                        if(comment_bool):
                            temp = self.driver.find_elements_by_tag_name("input")

                            #randomizes the comment list
                            comment_list = comment_text.split(",")
                            text = comment_list[randint(0, len(comment_list)-1)]

                            #send the text to input and submit
                            temp[0].send_keys(text)
                            self.driver.implicitly_wait(1)
                            temp[0].submit()
                            time.sleep(2)
                            return False
                    except Exception:
                        return True










        
