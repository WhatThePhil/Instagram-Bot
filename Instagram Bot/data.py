class Data():
    def __init__(self):
        self.username = ""
        self.password = ""
        self.gathered_users = []
        self.browser = ""
        self.unfollow_total = 0
     
    def add_users(self, usr):
        self.gathered_users.append(usr)

    def remove_begin_elem(self):
        self.gathered_users.pop(0)

    def set_username(self, usr):
        self.username = usr

    def set_pw(self, pw):
        self.password = pw

    def get_total(self):
        return len(self.gathered_users)

    def get_user_list(self):
        return self.gathered_users

    def get_username(self):
        return self.username

    def get_pw(self):
        return self.password
    
    def get_first_user(self):
        return self.gathered_users[0]

    def make_set(self):
        set(self.gathered_users)

    def set_browser(self, browser):
        self.browser = browser

    def get_browser(self):
        return self.browser

    def set_driver(self, driver):
        self.driver = driver

    def get_driver(self):
        return self.driver

    def update_unfollow_total(self):
        self.unfollow_total += 1

    def get_unfollow_total(self):
        return self.unfollow_total

    def decrement_unfollow_total(self):
        self.unfollow_total -= 1
