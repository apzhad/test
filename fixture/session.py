# -*- coding: utf-8 -*-


class SessionManage:

    def __init__(self, gen):
        self.gen = gen

    def login(self, username, password):
        wd = self.gen.wd
        self.gen.open_home_page()
        # enter username and password for login
        wd.find_element_by_name("user").click()
        wd.find_element_by_name("user").clear()
        wd.find_element_by_name("user").send_keys(username)
        wd.find_element_by_name("pass").clear()
        wd.find_element_by_name("pass").send_keys(password)
        # login
        wd.find_element_by_xpath("//input[@value='Login']").click()

    def logout(self):
        wd = self.gen.wd
        wd.find_element_by_link_text("Logout").click()
        wd.find_element_by_name("user")

    def ensure_logout(self):
        if self.is_login():
            self.logout()

    def ensure_login(self, username, password):
        if self.is_login():
            if self.is_login_as(username):
                return
            else:
                self.logout()
        self.login(username, password)

    def is_login(self):
        wd = self.gen.wd
        return len(wd.find_elements_by_link_text("Logout")) > 0

    def is_login_as(self, username):
        wd = self.gen.wd
        return self.get_logged_user() == username

    def get_logged_user(self):
        wd = self.gen.wd
        return wd.find_element_by_xpath("//div[@id='top']/form/b").text[1:-1]
