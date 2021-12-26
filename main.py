from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from hoverable import HoverBehavior
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
import json, glob
from datetime import datetime
from pathlib import Path
import random

Builder.load_file('design.kv')

class LoginScreen(Screen):
    def sign_up(self):
        self.manager.transition.direction = 'up'
        self.manager.current = "sign_up_screen"
    
    def forgot_pw(self):
        self.manager.transition.direction = 'down'
        self.manager.current = "forgot_password"

    def login(self, uname, pword):
        with open("users.json") as file:
            users = json.load(file)
        
        if uname in users and users[uname]['password'] == pword:
            self.ids.login_wrong.text = ""
            self.manager.transition.direction = 'left'
            self.manager.current = "login_screen_success"
        else:
            self.ids.login_wrong.text = "Wrong Username or Password."

class RootWidget(ScreenManager):
    pass

class SignUpScreen(Screen):
    def add_user(self, uname, pword):
        with open("users.json") as file:
            users = json.load(file)

        users[uname] = {'username': uname, 'password': pword,
                        'created': datetime.now().strftime("%Y-%m-%d %H-%H-%S")}

        with open("users.json", 'w') as file:
            json.dump(users, file)

        self.manager.transition.direction = 'left'
        self.manager.current = "sign_up_screen_success"

class SignUpScreenSuccess(Screen):
    def go_to_login(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "login_screen"

class ForgotPassword(Screen):
    def password_lookup(self,uname):
        with open("users.json") as file:
            users = json.load(file)

        for user in users:
            if user == uname:
                lost_pword = users[uname]['password']
                self.manager.transition.direction = 'down'
                #self.manager.ids.lost_pword.text = users[uname]['password']
                self.manager.current = "password_retrieve"
                return

        self.manager.transition.direction = 'down'
        self.manager.current = "password_not_found"

class PasswordRetrieve(Screen):
    lost_pword = "<Password here>"
    def go_to_login(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "login_screen"

class PasswordNotFound(Screen):
    def go_to_login(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "login_screen"    

class LoginScreenSuccess(Screen):
    def log_out(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "login_screen"

    def get_quote(self, feel):
        feel = feel.lower()
        available_feels = glob.glob("quotes/*txt")
        
        available_feels = [Path(filename).stem for filename in available_feels]

        if feel in available_feels:
            with open(f"quotes/{feel}.txt", encoding="UTF-8") as file:
                quotes = file.readlines()
            self.ids.quote.text = random.choice(quotes)
        else:
            self.ids.quote.text = f"Sorry, I don't know the feeling \"{feel}\"."
            
class ImageButton(ButtonBehavior, HoverBehavior, Image):
    pass

class MainApp(App):
    def build(self):
        self.title = "TEST TITLE" #Sets the window Title
        return RootWidget()

if __name__ == "__main__":
    MainApp().run()