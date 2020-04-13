# -*- coding: utf-8 -*-
from selenium import webdriver
from fixture.session import SessionManage
from fixture.group import GroupManage
from fixture.contact import ContactManage


class Generic:

    def __init__(self, browser, base_url):
        if browser == "firefox":
            self.wd = webdriver.Firefox()
        elif browser == "chrome":
            self.wd = webdriver.Chrome()
        elif browser == "edge":
            self.wd = webdriver.Edge()
        elif browser == "ie":
            self.wd = webdriver.Ie()
        else:
            raise ValueError("Unrecognized browser %s" % browser)
        self.base_url = base_url
        self.wd.implicitly_wait(1)
        self.session = SessionManage(self)
        self.group = GroupManage(self)
        self.contact = ContactManage(self)

    def open_home_page(self):
        wd = self.wd
        wd.get(self.base_url)

    def finish(self):
        self.wd.quit()

    def is_valid(self):
        try:
            self.wd.current_url
            return True
        except:
            return False
