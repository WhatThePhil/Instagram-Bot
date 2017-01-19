from InstaBot import Instagram
from LoginGUI import Login_GUI
from data import Data
import tkinter as tk
import time, copy
from selenium import webdriver
        
        
class InstaBot_GUI():
    def __init__(self, data, driver, master):
        self.driver = driver
        self.data = data
        self.master = master
        self.master.title("InstaBot")
        

    #header -- step one
        stepOne = tk.LabelFrame(self.master, text=" 1. Gather User Profiles: ")
        stepOne.grid(row=0, columnspan = 7, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)

        #create radio buttons / text entry
        self.v = tk.StringVar()
        self.v.set("commentor")
        commentor = tk.Radiobutton(stepOne, text="Commentors (from a post)", variable=self.v, value="commentor")
        commentor.grid(row=0, column=0, sticky='W', padx=5, pady=2)
        self.commentor_entry = tk.Entry(stepOne, width=40)
        self.commentor_entry.grid(row=0, column=1, sticky="WE", pady=3)

        followers = tk.Radiobutton(stepOne, text="Followers (from username)", variable=self.v, value="followers")
        followers.grid(row=1, column=0, sticky='W', padx=5, pady=2)
        self.follower_entry = tk.Entry(stepOne)
        self.follower_entry.grid(row=1, column=1, sticky="WE", pady=3)

        hashtag = tk.Radiobutton(stepOne, text="Hashtag", variable=self.v, value="hashtag")
        hashtag.grid(row=2, column=0, sticky='W', padx=5, pady=2)
        self.hash_entry = tk.Entry(stepOne)
        self.hash_entry.grid(row=2, column=1, sticky="WE", pady=3)

        self.total = tk.Label(stepOne, text="How many users to gather")
        self.total.grid(row=4, column=0, sticky='W', padx=5, pady=2)
        self.total_entry = tk.Entry(stepOne,width = 5)
        self.total_entry.grid(row=4, column=1, sticky='W', pady=2)


    #header -- step two
        stepTwo = tk.LabelFrame(self.master, text=" 2. Perform Actions: ")
        stepTwo.grid(row=1, columnspan=7, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)

        self.a = tk.IntVar()
        self.a.set(1)
        self.b = tk.IntVar()
        self.b.set(0)
        self.c = tk.IntVar()
        self.c.set(0)
        follow = tk.Checkbutton(stepTwo, text = "Follow", variable = self.a, onvalue = 1)
        follow.grid(row=0, column=0, sticky='W', padx=5, pady=2)
        follow = tk.Checkbutton(stepTwo, text = "Like Posts", variable = self.b, onvalue = 1)
        follow.grid(row=1, column=0, sticky='W', padx=5, pady=2)
        
        follow = tk.Checkbutton(stepTwo, text = "Comment", variable = self.c, onvalue = 1)
        follow.grid(row=2, column=0, sticky='W', padx=5, pady=2)
        self.comment = tk.Label(stepTwo, text="Enter your comments")
        self.comment.grid(row=2, column=1, sticky='W', padx=5, pady=2)

        entryText = "let's follow each other!, follow back?, I just followed ya! good stuff, Great Stuff, Wow I like it!, Brilliant, nice feed!, pretty sweet :), awesome, sick, really nice,  love it, this is awesome!, <3, very cool"
        self.comment_list = tk.Entry(stepTwo, width=40)
        self.comment_list.insert(0, entryText)
        self.comment_list.grid(row=2, column=2, sticky='W', pady=2)
        
        follow = tk.Checkbutton(stepTwo, text = "Unfollow", variable = self.a, onvalue = 2)
        follow.grid(row=3, column=0, sticky='W', padx=5, pady=2)
        self.totalUn = tk.Label(stepTwo, text="How many to unfollow?")
        self.totalUn.grid(row=3, column=1, sticky='W', padx=5, pady=2)
        self.total_unfollow = tk.Entry(stepTwo,width = 10)
        self.total_unfollow.grid(row=3, column=2, sticky='W', pady=2)

    #header -- step three
        stepThree = tk.LabelFrame(self.master, text=" 3. Filters: ")
        stepThree.grid(row=2, columnspan=7, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)

        self.f1 = tk.IntVar()
        self.f2 = tk.IntVar()
        self.f1.set(1)

        self.filter1 = tk.Checkbutton(stepThree, text = "Don't follow private users", variable = self.f1, onvalue = 1)
        self.filter1.grid(row=0, column=0, sticky='W', padx=5, pady=2)
        self.filter2 = tk.Checkbutton(stepThree, text = "Only unfollow users who don't follow you back", variable = self.f2, onvalue = 1, state=tk.DISABLED)
        self.filter2.grid(row=1, column=0, sticky='W', padx=5, pady=2)

    #header -- step four
        stepFour = tk.LabelFrame(self.master, text=" 4. Speed Of Actions: ")
        stepFour.grid(row=3, columnspan=7, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)

        self.slide1 = tk.Scale(stepFour, orient=tk.HORIZONTAL,from_=0, to=60, resolution=5, \
                          activebackground="LIGHTGREEN", label="(Un)Follows/hr", sliderlength = 20)
        self.slide1.grid(row=0, column=0, sticky='WE', padx=5, pady=2)
        self.slide1.set(60)

        self.slide2 = tk.Scale(stepFour, orient=tk.HORIZONTAL,from_=0, to=80, resolution=5, \
                          activebackground="LIGHTGREEN", label="Likes/hr", sliderlength = 20)
        self.slide2.grid(row=0, column=1, sticky='WE', padx=5, pady=2)
        self.slide2.set(30)

        self.slide3 = tk.Scale(stepFour, orient=tk.HORIZONTAL,from_=0, to=40, resolution=5, \
                          activebackground="LIGHTGREEN", label="Comments/hr", sliderlength = 20)
        self.slide3.grid(row=0, column=2, sticky='WE', padx=5, pady=2)
        self.slide3.set(10)

        self.note = tk.Label(stepFour, text="Limit: 150 actions/hr")
        self.note.grid(row=0, column=3, sticky='WN', padx=5, pady=2)
        
    #header -- step five
        

    #Start
        start = tk.Button(stepFour, text='START BOT', command=self.selected, relief=tk.RAISED)
        start.grid(row=0, column=3, sticky='S')


    def selected(self):
        insta = Instagram(self.data, self.driver)
        
        if(self.total_entry.get() != ""):
            self.check_gather(insta)
            total = self.data.get_total()
            print(str(total) + " total users")

        #actions per hour (slider values)
        self.followshr = self.slide1.get()
        self.likeshr = self.slide2.get()
        self.commentshr = self.slide3.get()
        action_total = (self.followshr + self.likeshr + self.commentshr)

        #check to make sure actions dont exceed 150
        if(action_total > 150):
            print("Error: Speed of actions is greater than 100")
            return

            
        #try to get an unfollow total, if no input throw exception
        try:
            unfollow_total = int(self.total_unfollow.get())
        except Exception:
            unfollow_total = 0

        try:
            follow_interval = 3600/self.followshr
        except Exception:
            follow_interval = 0

        try:
            like_interval = 3600/self.likeshr
        except Exception:
            like_interval = 0

        try:
            comment_interval = 3600/self.commentshr
        except Exception:
            comment_interval = 0

        #subtract by interval on intial time because we want to start actions at 0seconds
        start_time1 = time.time() - follow_interval - 1
        start_time2 = time.time() - like_interval - 1
        start_time3 = time.time() - comment_interval - 1

        follow_list = copy.deepcopy(self.data.get_user_list())
        like_list = copy.deepcopy(self.data.get_user_list())
        comment_list = copy.deepcopy(self.data.get_user_list())

        print("(Un)Follow Interval Every: " + str("{0:0.1f}".format(follow_interval/60)) + " minutes")
        print("Like Interval Every: " + str("{0:0.1f}".format(like_interval/60))+ " minutes")
        print("Comment Interval Every: " + str("{0:0.1f}".format(comment_interval/60))+ " minutes")

        current_followed = 0
        current_liked = 0
        current_commented = 0
        current_unfollowed = 0


        #if current time - interval is greater than the start time then we've gone over the interval limit
        #so we execute the while loop and update start time
        while(True):
            if(len(follow_list) == 0 and len(like_list) == 0 and len(comment_list) == 0 and unfollow_total == 0):
                return
               
            while(time.time() - follow_interval > start_time1):
                if(self.a.get() == 1):
                    not_followed = insta.follow(follow_list[0], self.f1.get())

                    while(not_followed and len(follow_list) > 1):
                        follow_list.pop(0)
                        not_followed = insta.follow(follow_list[0], self.f1.get())

                    follow_list.pop(0) 
                    current_followed +=1
                    print("Total Followed: " + str(current_followed))
                    start_time1 = time.time()
                elif(self.a.get() == 2 and unfollow_total > 0):
                    insta.unfollow()
                    current_unfollowed = self.data.get_unfollow_total()
                    unfollow_total = unfollow_total - 1
                    print("Total Unfollowed: " + str(current_unfollowed))
                    start_time1 = time.time()
                else:
                    start_time1 += 100000 
                    
            while(time.time() - like_interval > start_time2):
                if(like_interval == 0 or len(like_list) == 0):
                    start_time2 += 100000
                elif(self.b.get() == 1):
                    private = insta.comment_like(False, True, self.comment_list.get(), like_list[0])
                    
                    while(private and len(like_list) > 1):
                        if(self.c.get() == 1):
                            comment_list.remove(like_list[0])
                        like_list.pop(0)
                        private = insta.comment_like(False, True, self.comment_list.get(), like_list[0])
                        
                    like_list.pop(0)
                    current_liked +=1
                    print("Total Liked: " + str(current_liked))
                    start_time2 = time.time()
                else:
                    start_time2 += 100000 
                    
            while(time.time() - comment_interval > start_time3):
                if(comment_interval == 0 or len(comment_list) == 0):
                    start_time3 += 100000
                elif(self.c.get() == 1):
                    private = insta.comment_like(True, False, self.comment_list.get(), comment_list[0])
                    
                    while(private and len(comment_list) > 1):
                        comment_list.pop(0)
                        private = insta.comment_like(True, False, self.comment_list.get(), comment_list[0])
                        
                    comment_list.pop(0)
                    current_commented += 1
                    print("Total Comments: " + str(current_commented))
                    start_time3 = time.time()
                else:
                    start_time3 += 100000 
                  

    def check_gather(self, insta):
        if(self.v.get() == "commentor"):
            insta.gather_commentors(self.commentor_entry.get(), self.total_entry.get())
        elif(self.v.get() == "followers"):
            insta.gather_f(self.follower_entry.get(), self.total_entry.get(), 'follower')
        elif(self.v.get() == "following"):
            insta.gather_f(self.following_entry.get(), self.total_entry.get(), 'following')
        elif(self.v.get() == "hashtag"):
            insta.gather_hashtag(self.hash_entry.get(), self.total_entry.get())
        


class Frame():
    def __init__(self, userinfo, data):
        root = tk.Tk()
        self.data = data
        
        if(userinfo == "login"):
            login = Login_GUI(root, self.data)
        elif(userinfo == "bot"):
            driver = data.get_driver()
            driver.HideCommandPromptWindow = True;
            self.insta = InstaBot_GUI(self.data, driver, root)

        root.mainloop()



def main():

    #create driver
    #driver = webdriver.PhantomJS()
    #create GUI frame
    data = Data()

    Frame("login", data)
    driver = data.get_driver()
    insta = Instagram(data, driver)
    insta.login()
    data.set_driver(driver)
    Frame("bot", data)

    #to do
    #make liking and commenting and following modular
    #make it a small function to call
    #hashtag function -- gathers all the media posts up to N
    #once list is full will call actions likes, comment, follow
    #
    #like photos on feed up to certain date X (after done following)
    #add to follow function: if user has no posts or already following then skip users and go to next (return True)
    #seperate comment and like functionality
    #like posts on your feed

    

if __name__ == '__main__':
    main()
