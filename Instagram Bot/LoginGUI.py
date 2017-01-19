import tkinter as tk
from tkinter import *
from selenium import webdriver

class Login_GUI():
    def __init__(self, master, data):
        self.master = master
        self.data = data
        self.master.title("InstaBot")

    #header -- step one
        stepOne = tk.LabelFrame(self.master, text=" 1. Login ")
        stepOne.grid(row=0, columnspan=7, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)

        #create radio buttons / text entry

        Label(stepOne, text="Username").grid(row=0, column=0)
        Label(stepOne, text="Password").grid(row=1, column=0)

        self.e1 = Entry(stepOne)
        self.e2 = Entry(stepOne, show="*")

        self.e1.grid(row=0, column=1, sticky='WE')
        self.e2.grid(row=1, column=1, sticky='WE')

    #header -- step two
        stepTwo = tk.LabelFrame(self.master, text=" 2. Choose Browser ")
        stepTwo.grid(row=1, columnspan=7, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)

        self.v = tk.StringVar()
        self.v.set("ff")
        ff = tk.Radiobutton(stepTwo, text="Firefox", variable=self.v, value="ff")
        ff.grid(row=0, column=0, sticky='W', padx=5, pady=2)
        chrome = tk.Radiobutton(stepTwo, text="Chrome", variable=self.v, value="chrome", state = tk.DISABLED)
        chrome.grid(row=0, column=1, sticky='W', padx=5, pady=2)

        Button(stepTwo, text='Submit', command=self.button_action).grid(row=0, column=3, sticky=W, pady=4)
                
    def button_action(self):
        self.data.set_username(self.e1.get())
        self.data.set_pw(self.e2.get())
        self.data.set_browser(self.v.get())

        if(self.data.get_browser() == "ff"):
            driver = webdriver.Firefox()
            driver.set_window_size(500, 500)
            self.data.set_driver(driver)
        elif(self.data.get_browser() == "chrome"):
            driver = webdriver.Chrome()
            self.data.set_driver(driver)
            
        self.master.destroy()
        
