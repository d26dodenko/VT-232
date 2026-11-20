from pages.base_page import BasePage


class AuthPage(BasePage):
    NAME_INPUT = "input[name='name'], input[placeholder*='Name' i], input[type='text']"
    EMAIL_INPUT = "input[name='email'], input[type='email'], input[placeholder*='Email' i]"
    PASSWORD_INPUT = "input[name='password'], input[type='password'], input[placeholder*='Password' i]"
    SUBMIT_BTN = "button[type='submit']"
    LOGOUT_BTN = "button:has-text('Logout'), a:has-text('Logout'), button:has-text('Log out')"
    LOGIN_NAV_LINK = "a[href*='login'], button:has-text('Login')"

    def register_user(self, name: str, email: str, password: str):
        self.open_path("/signup")
        self.fill(self.NAME_INPUT, name)
        self.fill(self.EMAIL_INPUT, email)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.SUBMIT_BTN)

    def login_user(self, email: str, password: str):
        self.open_path("/login")
        self.fill(self.EMAIL_INPUT, email)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.SUBMIT_BTN)

    def logout_user(self):
        self.click(self.LOGOUT_BTN)
