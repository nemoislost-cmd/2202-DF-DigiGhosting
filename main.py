import datetime
import queue
import logging
import signal
import time
import threading
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk, VERTICAL, HORIZONTAL, N, S, E, W
import re
import pandas as pd
import openpyxl
from selenium import webdriver
import time
import undetected_chromedriver as uc  # pip install undetected_chromedriver required
import pyperclip as pc  # to output the content of clipboard into idle screen
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from tkinter import *  # python GUI

logger = logging.getLogger(__name__)


class Clock(threading.Thread):

    def __init__(self):
        super().__init__()
        self._stop_event = threading.Event()

    def run(self):
        logger.debug("Program is running......")
      


    def stop(self):
        self._stop_event.set()


class QueueHandler(logging.Handler):
    """Class to send logging records to a queue
    It can be used from different threads
    The ConsoleUi class polls this queue to display records in a ScrolledText widget
    """

    def __init__(self, log_queue):
        super().__init__()
        self.log_queue = log_queue

    def emit(self, record):
        self.log_queue.put(record)


class LoggingQueue:
    """Poll messages from a logging queue and display them in a scrolled text widget"""

    def __init__(self, frame):
        self.frame = frame
        # Create a ScrolledText wdiget
        self.scrolled_text = ScrolledText(frame, state="disabled", height=12)
        self.scrolled_text.grid(row=0, column=0, sticky=(N, S, W, E))
        self.scrolled_text.configure(font="TkFixedFont")
        self.scrolled_text.tag_config("INFO", foreground="black")
        self.scrolled_text.tag_config("DEBUG", foreground="blue")
        self.scrolled_text.tag_config("WARNING", foreground="orange")
        self.scrolled_text.tag_config("ERROR", foreground="red")
        self.scrolled_text.tag_config("CRITICAL", foreground="red", underline=1)
        # Create a logging handler using a queue
        self.log_queue = queue.Queue()
        self.queue_handler = QueueHandler(self.log_queue)
        formatter = logging.Formatter("%(asctime)s: %(message)s")
        self.queue_handler.setFormatter(formatter)
        logger.addHandler(self.queue_handler)
        # Start polling messages from the queue
        self.frame.after(100, self.poll_log_queue)

    def display(self, record):
        msg = self.queue_handler.format(record)
        self.scrolled_text.configure(state="normal")
        self.scrolled_text.insert(tk.END, msg + "\n", record.levelname)
        self.scrolled_text.configure(state="disabled")
        # Autoscroll to the bottom
        self.scrolled_text.yview(tk.END)

    def poll_log_queue(self):
        # Check every 100ms if there is a new message in the queue to display
        while True:
            try:
                record = self.log_queue.get(block=False)
            except queue.Empty:
                break
            else:
                self.display(record)
        self.frame.after(100, self.poll_log_queue)


class MainGUI:
    def __init__(self, frame):  ##### creating the main gui #####
        self.frame = frame
        self.UserEmail = tk.StringVar()
        self.UserPassword = tk.StringVar()
        self.WebName1 = tk.IntVar()
        self.WebName2 = tk.IntVar()
        self.WebName3 = tk.IntVar()
        self.WebName4 = tk.IntVar()
        ttk.Label(frame, text="Email").grid(column=0, row=0, sticky=W)
        ttk.Label(frame, text="Password").grid(column=0, row=1, sticky=W)
        ttk.Button(frame, text="Login", command=self.validateLogin).grid(
            row=2, column=1, sticky=W
        )
        ttk.Entry(frame, textvariable=self.UserEmail).grid(row=0, column=1, sticky=W)
        ttk.Entry(frame, textvariable=self.UserPassword).grid(row=1, column=1, sticky=W)
        ttk.Label(
            frame,
            text="Method 1 (Google Password Manager) : Indicate Website(s) to delete data from!",
        ).grid(row=3, column=0, sticky=W)
        self.chkbtn1 = ttk.Checkbutton(
            frame,
            text="Facebook",
            variable=self.WebName1,
            onvalue=1,
            offvalue=0,
            state="disabled",
        )  # by default state is disabled
        self.chkbtn1.grid(row=4, sticky=W)
        self.chkbtn2 = ttk.Checkbutton(
            frame,
            text="Reddit",
            variable=self.WebName2,
            onvalue=1,
            offvalue=0,
            state="disabled",
        )
        self.chkbtn2.grid(row=5, sticky=W)
        self.chkbtn3 = ttk.Checkbutton(
            frame,
            text="Pinterest",
            variable=self.WebName3,
            onvalue=1,
            offvalue=0,
            state="disabled",
        )
        self.chkbtn3.grid(row=6, sticky=W)
        self.chkbtn4 = ttk.Checkbutton(
            frame,
            text="Discord",
            variable=self.WebName4,
            onvalue=1,
            offvalue=0,
            state="disabled",
        )
        self.chkbtn4.grid(row=7, sticky=W)
        self.submitBtn= ttk.Button(frame, text="Submit", command=self.validateSubmit , state="disabled")
        self.submitBtn.grid(row=8,column=1 , sticky=E)

    def validateLogin(self):
        logger.info("Validating Credentials....")
        regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b" #regex string to validate if email format is correct test.gmail.com is an eg of an invalid input
        if re.fullmatch(regex, self.UserEmail.get()):  # validating email format
            if (
                "gmail" in self.UserEmail.get()
            ):  # if gmail only checkboxes will be made visible
                logger.info("Validated Credentials.....")
                logger.info("Waiting for User Input....")
                self.chkbtn1.state(["!disabled"])  # making the buttons visible
                self.chkbtn2.state(["!disabled"])  # ensuring that selection can only be recorded if email is valid and its a gmail
                self.chkbtn3.state(["!disabled"])
                self.chkbtn4.state(["!disabled"])
                self.submitBtn.state(['!disabled'])
        else:
            logger.error("Invalid email.. Try again.")

    def facebookredirect(self,driver,website_username, website_pw, start):  # function that deletes account from Facebook
        driver.get("https://www.facebook.com")
        driver.implicitly_wait(3)
        Facebook_username_field = driver.find_element(By.NAME, "email")
        Facebook_username_field.send_keys(website_username)
        driver.implicitly_wait(3)
        Facebook_password_field = driver.find_element(By.NAME, "pass")
        Facebook_password_field.send_keys(website_pw)
        driver.implicitly_wait(3)
        driver.find_element(By.XPATH, "//*[text()='Log in']").click()
        time.sleep(1)
        end = time.perf_counter()  # calculate runtime of program
        logger.info("Login Successful for facebook.com")
        ######deletion portion here to be added#######
        logger.info("Processing to delete facebook account")
        driver.get("https://www.facebook.com/deactivate_delete_account/")
        XPATH_DeleteAccount = "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div/div/div/div/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[1]/label/div/input"
        driver.find_element(By.XPATH, XPATH_DeleteAccount).click()
        XPATH_ContinueToAccDele = "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div/div/div/div/div/div/div/div[3]/div/div[2]/a/div/div[1]/div/span/span"
        driver.find_element(By.XPATH, XPATH_ContinueToAccDele).click()
        XPATH_ConfirmDeleteAcc = "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div/div/div/div/div/div/div/div[2]/div/div[2]/div/div/div[1]/div/span/span"
        driver.find_element(By.XPATH, XPATH_ConfirmDeleteAcc).click()
        XPATH_ConfirmPassToDele = "/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div[1]/div[3]/div[1]/div/div[3]/div/div/form/div/label/div/div/input"
        driver.find_element(By.XPATH, XPATH_ConfirmPassToDele).send_keys(website_pw)
        time.sleep(2)
        ## next step should click continue [ uncomment the two line to continue delete account ]
        XPATH_ContinueButton = "/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div[1]/div[3]/div[2]/div[2]/div[1]/div/div[1]/div/span/span"
        driver.find_element(By.XPATH, XPATH_ContinueButton).click()
        driver.find_element(By.XPATH,"/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div[4]/div[2]/div[2]/div[1]/div").click()
        logger.info(f"Facebook finished in {end - start:0.4f} seconds")

    def GooglePasswordManagerThread(self, webDelete): #seperate thread that runs concurrently with the GUI
        Email = self.UserEmail.get()
        Pass = self.UserPassword.get()
        logger.info("Instantiating Google Chrome....")
        c = webdriver.ChromeOptions()
        c.add_argument("--ingonito") #ensure that data is not cached or stored in the history
        s = Service("C:\\webdrivers\\chromedriver.exe")
        driver = webdriver.Chrome(service=s)
        start = time.perf_counter()  # start the timer
        options = uc.ChromeOptions()
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_experimental_option(  # Disable save password popup in google chrome
            "prefs",
            {
                "credentials_enable_service": False, #To prevent chrome save password to popup
                "profile.password_manager_enabled": False,
                "profile.default_content_setting_values.notifications": 2,

            },
        )

        driver = uc.Chrome(options=options, use_subprocess=True)
        logger.info("Running Google Chrome....")
        logger.info("Logging into GMAIL...")
        driver.get(
            "https://accounts.google.com/v3/signin/identifier?dsh=S-619823408%3A1665628892681054&continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&rip=1&sacu=1&service=mail&flowName=GlifWebSignIn&flowEntry=ServiceLogin&ifkv=AQDHYWqtTkU3kxwPOaBJfFYgotOafgZ-4hHY_zs3a6wtZIZ5kbEydRMSfvO_ySHxmDStvxvipYvrxw"
        )
        driver.implicitly_wait(4)
        time.sleep(2)
        EleEmail = driver.find_element(By.NAME, "identifier")
        EleEmail.send_keys(f"{Email}\n")
        driver.implicitly_wait(5)
        ElePass = driver.find_element(By.NAME, "Passwd")
        ElePass.send_keys(f"{Pass}\n")
        driver.implicitly_wait(3)
        time.sleep(5)
        driver.refresh()
        logger.info("Logged into GMAIL...")
        logger.info("Switching to Google Password Manager")
        websiteCredential = self.googlePassManager(webDelete, driver) #function invoked here. this function will extract the credentials from Google Password Manager
        logger.info("Credentials Extracted...")
        logger.info("Proceeding for deletion..")
        for website in webDelete:    ##### portion to be extended upon for more website ##### 
            if website == 'Facebook':
                logger.info("Logging into Facebook...")
                self.facebookredirect(driver,websiteCredential['Facebook'][0],websiteCredential['Facebook'][1],start)
            elif website=='Reddit':
                logger.info("Logging into Reddit....")
                self.redditredirect(driver,websiteCredential['Reddit'][0],websiteCredential['Reddit'][1],start)
            elif website=='Pinterest':
                logger.info("Logging into Pinterest...")
                self.pinterestredirect(driver,start)

            elif website=='Discord':
                logger.info("Logging into Discord...")
                self.discordredirect(driver,websiteCredential['Discord'][0],websiteCredential['Discord'][1],start)

        logger.info("Program Completed...")
    def discordredirect(self,driver,website_username,website_pw,start):
        driver.get("https://discord.com/login")
        driver.implicitly_wait(2)
        DISCORD_USERNAME=driver.find_element(By.XPATH,"//*[@id='uid_5']")
        DISCORD_PASSWORD=driver.find_element(By.XPATH,"//*[@id='uid_8']")
        DISCORD_USERNAME.send_keys(website_username)
        driver.implicitly_wait(2)
     
        DISCORD_PASSWORD.send_keys(website_pw)
        driver.implicitly_wait(2)
        driver.find_element(By.XPATH,"/html/body/div[2]/div[2]/div/div[1]/div/div/div/div/form/div/div/div[1]/div[2]/button[2]").click()
        time.sleep(5)
        driver.implicitly_wait(4)
        driver.find_element(By.XPATH,"//*[@id='app-mount']/div[2]/div/div[1]/div/div[2]/div/div[1]/div/div/div/section/div[2]/div[2]/button[3]").click()
        driver.implicitly_wait(4)
        driver.find_element(By.XPATH,"//*[@id='my-account-tab']/div/div[5]/div[2]/div[2]/button[2]").click()
        DISCORD_RE_PW=driver.find_element(By.XPATH,"//*[@id='app-mount']/div[2]/div/div[3]/div[2]/div/div/form/div[2]/div[2]/div/input")
        driver.implicitly_wait(2)
        DISCORD_RE_PW.send_keys(f"{website_pw}\n")
        #driver.find_element(By.XPATH,"//*[@id='app-mount']/div[2]/div/div[3]/div[2]/div/div/form/div[3]/button[1]").click()
        driver.implicitly_wait(1)
        end = time.perf_counter()
        logger.info(f"Discord deletion finished in {end - start:0.4f} seconds")
        
        
        
        

    def redditredirect(self,driver,website_username, website_pw, start):
        driver.get(
            "https://www.reddit.com/login/?dest=https%3A%2F%2Fwww.reddit.com%2F"
        )  # log in url for reddit
        Reddit_UserName_Field = driver.find_element(
            By.XPATH, "//*[@id='loginUsername']"
        )
        Reddit_UserName_Field.send_keys(f"{website_username}\n")
        driver.implicitly_wait(3)
        Reddit_Password_Field = driver.find_element(
            By.XPATH, "//*[@id='loginPassword']"
        )
        Reddit_Password_Field.send_keys(f"{website_pw}\n")
        driver.implicitly_wait(3)
        time.sleep(1)
        logger.info("Login Successful for reddit.com")
        driver.implicitly_wait(6)
        driver.get("https://www.reddit.com/settings/")
        driver.implicitly_wait(5)
        driver.find_element(By.XPATH,"//*[@id='AppRouter-main-content']/div/div[2]/div[1]/div[12]/button").click()
        driver.implicitly_wait(3)
        Username_Deletion_Field=driver.find_element(By.XPATH,"//*[@id='SHORTCUT_FOCUSABLE_DIV']/div[4]/div/div/div/div/div[1]/input")
        Password_Deletion_Field=driver.find_element(By.XPATH,"//*[@id='SHORTCUT_FOCUSABLE_DIV']/div[4]/div/div/div/div/div[2]/input")
        Username_Deletion_Field.send_keys(f"{website_username}\n")
        Password_Deletion_Field.send_keys(f"{website_pw}\n")
        driver.find_element(By.XPATH,"//*[@id='SHORTCUT_FOCUSABLE_DIV']/div[4]/div/div/div/div/div[3]/button").click()
        driver.find_element(By.XPATH,"//*[@id='SHORTCUT_FOCUSABLE_DIV']/div[4]/div/div/div/div/div[4]/button[2]").click()
        driver.implicitly_wait(4)
        #driver.find_element(By.XPATH,"//*[@id='SHORTCUT_FOCUSABLE_DIV']/div[4]/div/div/div/div/div[4]/button[2]").click()
        driver.find_element(By.XPATH,"//*[@id='SHORTCUT_FOCUSABLE_DIV']/div[4]/div/div/div/div/div/button[2]").click()
        end = time.perf_counter()  # calculate runtime of program
        logger.info(f"Reddit deletion finished in {end - start:0.4f} seconds")
    def pinterestredirect(self, driver, start):
        driver.get("https://www.pinterest.com/login/")
        time.sleep(10) # when redirect, it will autologin w google credential
        end = time.perf_counter()  # calculate runtime of program
        logger.info("Login Successful for pinterest.com")
        logger.info("Proceeding to delete pinterest account...")
        driver.get("https://www.pinterest.com/close-account")
        XPATH_ContinueBnEmail = "/html/body/div[1]/div[1]/div/div/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[3]/button/div/div"
        driver.find_element(By.XPATH, XPATH_ContinueBnEmail).click()
        XPATH_OtherRadioBn = "/html/body/div[3]/div/div/div/div[2]/div/div[2]/form/div/fieldset/div/div[5]/div/div/div[1]/div/div[1]"
        driver.find_element(By.XPATH, XPATH_OtherRadioBn).click()
        XPATH_SendEmail = "/html/body/div[3]/div/div/div/div[2]/div/div[3]/div/div/button/div"
        driver.find_element(By.XPATH, XPATH_SendEmail).click()
        time.sleep(5)
        driver.get("https://mail.google.com/mail/u/0/#inbox")
        driver.implicitly_wait(3)
        time.sleep(5)
        driver.get("https://mail.google.com/mail/u/0/#inbox")
        XPATH_ClickPinterestEmail = "/html/body/div[7]/div[3]/div/div[2]/div[2]/div/div/div/div/div[2]/div/div[1]/div/div/div[8]/div/div[1]/div[2]/div/table/tbody/tr[1]/td[5]/div/div/div/span/span"
        driver.find_element(By.XPATH, XPATH_ClickPinterestEmail).click()
        XPATH_DeletePinterestAcc = "/html/body/div[7]/div[3]/div/div[2]/div[2]/div/div/div/div/div[2]/div/div[1]/div/div[2]/div/table/tr/td/div[2]/div[2]/div/div[3]/div/div/div/div/div/div[1]/div[2]/div[3]/div[3]/div/div[2]/table[12]/tbody/tr/td/div/table/tbody/tr/td/a"
        driver.find_element(By.XPATH, XPATH_DeletePinterestAcc).click()
        #Delete the mail after deleting your acc
        XPATH_DeleteEmailAfterDeleteAcc = "/html/body/div[7]/div[3]/div/div[2]/div[2]/div/div/div/div/div[1]/div[2]/div[1]/div/div[2]/div[3]/div"
        driver.find_element(By.XPATH, XPATH_DeleteEmailAfterDeleteAcc).click()
        logger.info(f"Pinterest deletion finished in {end - start:0.4f} seconds")

    def googlePassManager(self, webDelete, driver):
        Email = self.UserEmail.get()
        Pass = self.UserPassword.get()
        websiteCredential = {}
        driver.get(
            "https://passwords.google.com/?utm_source=chrome&utm_medium=desktop&utm_campaign=chrome_settings"
        )
        time.sleep(5)
        X_PATH_GooglePassMger = "//*[@id='yDmH0d']/c-wiz/div/div[3]/c-wiz/div/c-wiz/c-wiz[1]/div/div/div[1]/div/div[1]/div/div[1]/input"
        SearchPass = driver.find_element(By.XPATH, X_PATH_GooglePassMger)
        for (
            website
        ) in (
            webDelete
        ):  # website need to be dynamic based on what the user want to delete
            SearchPass.send_keys(website)
            logger.info("searching credentials for website: " + website)
            driver.implicitly_wait(5)
            X_PATH_SEARCH = "//*[@id='yDmH0d']/c-wiz/div/div[3]/c-wiz/div/c-wiz/c-wiz[1]/div/div/div[3]/div/div/ul/li/div[1]/a/div"
            driver.find_element(By.XPATH, X_PATH_SEARCH).click()
            driver.implicitly_wait(5)
            ElePass = driver.find_element(By.NAME, "password")
            ElePass.send_keys(f"{Pass}\n")
            driver.implicitly_wait(5)
            # copy the username of the website
            driver.find_element(
                By.XPATH,
                "//*[@id='yDmH0d']/c-wiz/div/div[3]/c-wiz/c-wiz/div/div[1]/c-wiz/div/div/div/div[2]/div[1]/div/div/div/div/button/span",
            ).click()
            driver.implicitly_wait(2)
            time.sleep(5)
            website_username = pc.paste()  # output the last item pasted onto clipboard

            # copy the password of the website
            driver.implicitly_wait(2)
            driver.find_element(
                By.XPATH,
                "//*[@id='yDmH0d']/c-wiz/div/div[3]/c-wiz/c-wiz/div/div[1]/c-wiz/div/div/div/div[2]/div[2]/div/div/div[2]/div/button/span",
            ).click()
            driver.implicitly_wait(2)
            website_pw = pc.paste()  # output the last item pasted onto clipboard

            # have to create a dictionary where is the key is the website and value is a tuple storing the username and password 
            websiteCredential[website]=(website_username,website_pw)
            # need do another website search
            driver.get(
                "https://passwords.google.com/?utm_source=chrome&utm_medium=desktop&utm_campaign=chrome_settings"
            )
            time.sleep(5)
            X_PATH_GooglePassMger = "//*[@id='yDmH0d']/c-wiz/div/div[3]/c-wiz/div/c-wiz/c-wiz[1]/div/div/div[1]/div/div[1]/div/div[1]/input"
            SearchPass = driver.find_element(By.XPATH, X_PATH_GooglePassMger)
        return websiteCredential

    def validateSubmit(self):

        logger.info("User Input Recieved...")
        logger.info("Validating User Input..")

        if "gmail" in self.UserEmail.get():
            websiteDelete = [] # storing the websites to delete the data from in a list
            if self.WebName1.get() == 1:
                websiteDelete.append("Facebook")
            if self.WebName2.get() == 1:
                websiteDelete.append("Reddit")
            if self.WebName3.get() == 1:
                websiteDelete.append("Pinterest")
            if self.WebName4.get() == 1:
                websiteDelete.append("Discord")

            if (
                len(websiteDelete) == 0
            ):  # checking for no selection will not let them proceed
                logger.error("No Website Selected. Please select one or more website.")
            else:
                msg = ""
                for site in websiteDelete:
                    msg += site + "|"
                logger.info("Selection recorded...")
                logger.info("Proceeding for deletion for websites " + msg + "....")
                x = threading.Thread(
                    target=self.GooglePasswordManagerThread, args=(websiteDelete,) #thread function invoked here
                )
                x.start()
                #####google password manager portion###############


class SecondaryGUI:
    def __init__(self, frame):
        self.frame = frame
        ttk.Label(self.frame, text="How this program works.....").grid(
            column=0, row=1, sticky=W
        )
        ttk.Label(self.frame, text="Key in your gmail and password and watch the automated deletion process!").grid(
            column=0, row=4, sticky=W
        )


class MainApplication:
    def __init__(self, root):
        self.root = root
        root.title("Digi-Ghosting")
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        # Create the panes and frames
        vertical_pane = ttk.PanedWindow(self.root, orient=VERTICAL)
        vertical_pane.grid(row=0, column=0, sticky="nsew")
        horizontal_pane = ttk.PanedWindow(vertical_pane, orient=HORIZONTAL)
        vertical_pane.add(horizontal_pane)
        form_frame = ttk.Labelframe(horizontal_pane, text="GUI")
        form_frame.columnconfigure(1, weight=1)
        horizontal_pane.add(form_frame, weight=1)
        console_frame = ttk.Labelframe(horizontal_pane, text="Console")
        console_frame.columnconfigure(0, weight=1)
        console_frame.rowconfigure(0, weight=1)
        horizontal_pane.add(console_frame, weight=1)
        third_frame = ttk.Labelframe(vertical_pane, text="Instructions")
        vertical_pane.add(third_frame, weight=1)
        # Initialize all frames
        self.form = MainGUI(form_frame)
        self.console = LoggingQueue(console_frame)
        self.third = SecondaryGUI(third_frame)
        self.clock = Clock()
        self.clock.start()
        self.root.protocol("WM_DELETE_WINDOW", self.quit)
        self.root.bind("<Control-q>", self.quit)
        signal.signal(signal.SIGINT, self.quit)

    def quit(self, *args):
        self.clock.stop()
        self.root.destroy()


def main():
    logging.basicConfig(level=logging.DEBUG)
    root = tk.Tk()
    app = MainApplication(root)
    app.root.mainloop()


if __name__ == "__main__":
    main()
