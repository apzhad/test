# -*- coding: utf-8 -*-
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
from model.contact import Contact
import re


class ContactManage:

    def __init__(self, gen):
        self.gen = gen

    def open_home_page(self):
        wd = self.gen.wd
        if "?group=" in wd.current_url and len(wd.find_elements_by_name('searchstring')) > 0:
            self.select_from_list(list_name="group", text="[all]")
            self.contact_cache = None
        elif not (wd.current_url.endswith("/addressbook/") and len(wd.find_elements_by_name('searchstring')) > 0):
            wd.find_element_by_link_text("home").click()
        WebDriverWait(wd, 10).until(EC.presence_of_element_located((By.LINK_TEXT, 'Last name')))

    def select_all_contact(self):
        wd = self.gen.wd
        # get contact count
        contact_count = self.get_contact_count()
        for i in range(contact_count):
            wd.find_element_by_xpath("(//input[@name='selected[]'])[%s]" % (i + 1)).click()

    def get_contact_count(self, group_name=None):
        wd = self.gen.wd
        # wd.find_element_by_link_text("home").click()
        if group_name is not None:
            self.open_contact_group(group_name)
        else:
            self.open_home_page()
        return len(wd.find_elements_by_name("selected[]"))

    def get_result_count(self, search, group_name=None):
        wd = self.gen.wd
        self.open_home_page()
        if group_name is not None:  # if search in defined group
            self.select_from_list("group", group_name)
        self.set_field_value("searchstring", search)
        return int(wd.find_element_by_id("search_count").text)

    def enter_contact_parameters(self, contact):
        wd = self.gen.wd
        # contact name
        self.set_field_value("firstname", contact.first_name)
        self.set_field_value("middlename", contact.middle_name)
        self.set_field_value("lastname", contact.last_name)
        self.set_field_value("nickname", contact.nickname)

        # add photo
        if contact.photo_path:
            photo = wd.find_element_by_name("photo")
            photo.send_keys(os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "..\\data\\contact_foto\\%s" % contact.photo_path))

        if contact.del_foto:
            wd.find_element_by_name("delete_photo").click()

        # common info (company, address,title, etc.)
        self.set_field_value("title", contact.title)
        self.set_field_value("company", contact.company)
        self.set_field_value("address", contact.address)
        # phone info
        self.set_field_value("home", contact.home_phone)
        self.set_field_value("mobile", contact.mobile_phone)
        self.set_field_value("work", contact.work_phone)
        self.set_field_value("fax", contact.fax)

        # email info
        self.set_field_value("email", contact.primary_email)
        self.set_field_value("email2", contact.secondary_email)
        self.set_field_value("email3", contact.third_email)
        self.set_field_value("homepage", contact.homepage)

        # birthday info
        self.select_from_list("bday", contact.birth_day)
        self.select_from_list("bmonth", contact.birth_month)
        self.set_field_value("byear", contact.birth_year)

        # anniversary info
        self.select_from_list("aday", contact.anniversary_day)
        self.select_from_list("amonth", contact.anniversary_month)
        self.set_field_value("ayear", contact.anniversary_year)

        # select group using group_id
        if contact.group_name:
            self.select_from_list_by_id("new_group", contact.group_name)

        # secondary info
        self.set_field_value("address2", contact.secondary_address)
        self.set_field_value("phone2", contact.secondary_home_phone)
        self.set_field_value("notes", contact.notes)

    def select_from_list(self, list_name, text):
        wd = self.gen.wd
        if text is not None:
            wd.find_element_by_name(list_name).click()
            Select(wd.find_element_by_name(list_name)).select_by_visible_text(text)

    def select_from_list_by_id(self, list_name, id):
        wd = self.gen.wd
        if id is not None:
            wd.find_element_by_name(list_name).click()
            wd.find_element_by_css_selector("select[name='%s'] > option[value='%s']" % (list_name, id)).click()

    def set_field_value(self, field_name, text):
        wd = self.gen.wd
        if text is not None:
            wd.find_element_by_name(field_name).click()
            wd.find_element_by_name(field_name).clear()
            wd.find_element_by_name(field_name).send_keys(text)

    def create(self, contact):
        wd = self.gen.wd
        self.init_create_contact()
        # enter contact parameters
        self.enter_contact_parameters(contact)
        # submit contact creation
        wd.find_element_by_xpath("(//input[@name='submit'])[2]").click()
        self.return_to_homepage()
        self.contact_cache = None

    def init_create_contact(self):
        wd = self.gen.wd
        if not (wd.current_url.endswith("/edit.php") and len(wd.find_elements_by_name("submit")) > 0):
            wd.find_element_by_link_text("add new").click()

    def return_to_homepage(self):
        wd = self.gen.wd
        wd.find_element_by_link_text("home page").click()
        WebDriverWait(wd, 10).until(EC.presence_of_element_located((By.LINK_TEXT, 'Last name')))

    def select_first_contact(self):
        wd = self.gen.wd
        wd.find_element_by_name("selected[]").click()

    def select_contact_by_index(self, index):
        wd = self.gen.wd
        wd.find_elements_by_name("selected[]")[index].click()

    def select_contact_by_id(self, id):
        wd = self.gen.wd
        wd.find_element_by_css_selector("input[value='%s']" % id).click()

    def create_empty(self):
        wd = self.gen.wd
        # init new contact creation
        self.init_create_contact()
        wd.find_element_by_xpath("(//input[@name='submit'])[2]").click()
        self.return_to_homepage()
        self.contact_cache = None

    def del_first(self):
        self.del_by_index(0)

    def del_by_index(self, index):
        wd = self.gen.wd
        self.open_home_page()
        # select first contact & submit deletion
        self.select_contact_by_index(index)
        wd.find_element_by_xpath("(//input[@value='Delete'])").click()
        wd.switch_to_alert().accept()
        self.wait_close_message_box()
        self.contact_cache = None

    def del_by_id(self, id):
        wd = self.gen.wd
        self.open_home_page()
        # select first contact & submit deletion
        self.select_contact_by_id(id)
        wd.find_element_by_xpath("(//input[@value='Delete'])").click()
        wd.switch_to_alert().accept()
        self.wait_close_message_box()
        self.contact_cache = None

    def wait_close_message_box(self):
        wd = self.gen.wd
        try:
            WebDriverWait(wd, 10).until(EC.invisibility_of_element((By.CLASS_NAME, 'msgbox')))
        except:
            print("Failed to return to homepage")

    def cancel_del_first(self):
        self.cancel_del_by_index(0)

    def cancel_del_by_index(self, index):
        wd = self.gen.wd
        self.open_home_page()
        # select contact & submit deletion
        self.select_contact_by_index(index)
        wd.find_element_by_xpath("(//input[@value='Delete'])").click()
        wd.switch_to_alert().dismiss()
        self.contact_cache = None

    def cancel_del_by_id(self, id):
        wd = self.gen.wd
        self.open_home_page()
        # select contact & submit deletion
        self.select_contact_by_id(id)
        wd.find_element_by_xpath("(//input[@value='Delete'])").click()
        wd.switch_to_alert().dismiss()
        self.contact_cache = None

    def del_by_select_all(self):
        wd = self.gen.wd
        self.open_home_page()
        # click "select all" & submit deletion
        wd.find_element_by_xpath("(//input[@id='MassCB'])").click()
        wd.find_element_by_xpath("(//input[@value='Delete'])").click()
        wd.switch_to_alert().accept()
        self.wait_close_message_box()
        self.contact_cache = None

    def del_all_by_click(self):
        wd = self.gen.wd
        self.open_home_page()
        self.select_all_contact()
        wd.find_element_by_xpath("(//input[@value='Delete'])").click()
        wd.switch_to_alert().accept()
        self.wait_close_message_box()
        self.contact_cache = None

    def del_unselected(self):
        wd = self.gen.wd
        self.open_home_page()
        wd.find_element_by_xpath("(//input[@value='Delete'])").click()
        wd.switch_to_alert().accept()
        self.contact_cache = None

    def del_all_from_group(self, group_id):
        wd = self.gen.wd
        self.open_contact_group(group_id)
        # click "select all" & submit deletion
        wd.find_element_by_xpath("(//input[@id='MassCB'])").click()
        wd.find_element_by_xpath("(//input[@value='Delete'])").click()
        wd.switch_to_alert().accept()
        self.wait_close_message_box()
        self.contact_cache = None

    def open_contact_group(self, group_id):
        wd = self.gen.wd
        if len(wd.find_elements_by_xpath("(//input[@id='MassCB'])")) > 0 and \
                len(wd.find_elements_by_name('searchstring')) > 0:
            if not (wd.current_url.endswith("addressbook/?group=" + group_id)):
                self.select_from_list_by_id("group", group_id)
                self.contact_cache = None
        else:
            wd.find_element_by_link_text("home").click()
            self.select_from_list_by_id("group", group_id)
            self.contact_cache = None

    def get_group_id(self, group):
        wd = self.gen.wd
        # todo: get id from fixture group. Maybe should use wd.back?
        if wd.find_element_by_xpath('//select[@name="group"]'):
            select = Select(wd.find_element_by_xpath('//select[@name="group"]'))
            for option in select.options:
                if option.text == group:
                    return str(option.get_attribute('value'))

    def del_first_from_group(self, group_name):
        self.del_from_group_by_index(0, group_name)

    def del_from_group_by_index(self, index, group_name):
        wd = self.gen.wd
        self.open_contact_group(group_name)
        # click "select all" & submit deletion
        self.select_contact_by_index(index)
        wd.find_element_by_xpath("(//input[@value='Delete'])").click()
        wd.switch_to_alert().accept()
        self.wait_close_message_box()
        self.contact_cache = None

    def del_from_group_by_id(self, contact_id, group_id):
        wd = self.gen.wd
        self.open_contact_group(group_id)
        self.select_contact_by_id(contact_id)
        wd.find_element_by_xpath("(//input[@value='Delete'])").click()
        wd.switch_to_alert().accept()
        self.wait_close_message_box()
        self.contact_cache = None

    def del_first_using_edit(self):
        self.del_using_edit_by_index(0)

    def del_using_edit_by_index(self, index):
        wd = self.gen.wd
        self.open_edit(index)
        wd.find_element_by_xpath("//input[@value='Delete']").click()
        self.wait_close_message_box()
        self.contact_cache = None

    def del_using_edit_by_id(self, id):
        wd = self.gen.wd
        self.open_edit_by_id(id)
        wd.find_element_by_xpath("//input[@value='Delete']").click()
        self.wait_close_message_box()
        self.contact_cache = None

    def open_edit(self, index, group=None, search=None):
        wd = self.gen.wd
        if group is not None:
            self.open_contact_group(group)
        else:
            self.open_home_page()
        if search is not None:
            self.set_field_value("searchstring", search)
        self.click_pencil_img(index)

    def open_edit_by_id(self, id, group=None, search=None):
        wd = self.gen.wd
        if group is not None:
            self.open_contact_group(group)
        else:
            self.open_home_page()
        if search is not None:
            self.set_field_value("searchstring", search)
        self.click_pencil_by_id(id)

    def edit_first(self, contact):
        self.edit_by_index(0, contact)

    def edit_by_index(self, index, contact):
        wd = self.gen.wd
        self.open_edit(index)
        self.enter_contact_parameters(contact)
        wd.find_element_by_name("update").click()
        self.return_to_homepage()
        self.contact_cache = None

    def edit_by_id(self, id, contact):
        wd = self.gen.wd
        self.open_edit_by_id(id)
        self.enter_contact_parameters(contact)
        wd.find_element_by_name("update").click()
        self.return_to_homepage()
        self.contact_cache = None

    def edit_first_wo_change(self):
        self.edit_wo_change_by_index(0)

    def edit_wo_change_by_index(self, index):
        wd = self.gen.wd
        self.open_edit(index)
        wd.find_element_by_name("update").click()
        self.return_to_homepage()
        self.contact_cache = None

    def edit_wo_change_by_id(self, id):
        wd = self.gen.wd
        self.open_edit_by_id(id)
        wd.find_element_by_name("update").click()
        self.return_to_homepage()
        self.contact_cache = None

    def edit_first_from_details(self, contact):
        wd = self.gen.wd
        self.edit_from_details_by_index(0, contact)

    def edit_from_details_by_index(self, index, contact):
        wd = self.gen.wd
        self.open_details(index)
        wd.find_element_by_name("modifiy").click()
        self.enter_contact_parameters(contact)
        wd.find_element_by_name("update").click()
        self.return_to_homepage()
        self.contact_cache = None

    def edit_from_details_by_id(self, id, contact):
        wd = self.gen.wd
        self.open_home_page()
        self.open_details_by_id(id)
        wd.find_element_by_name("modifiy").click()
        self.enter_contact_parameters(contact)
        wd.find_element_by_name("update").click()
        self.return_to_homepage()
        self.contact_cache = None

    def open_details(self, index):
        wd = self.gen.wd
        self.open_home_page()
        wd.find_elements_by_xpath("//img[@alt='Details']")[index].click()

    def open_details_by_id(self, id):
        wd = self.gen.wd
        wd.find_element_by_xpath("//a[@href='view.php?id=%s']" % id).click()

    def edit_first_in_group(self, group_name, contact):
        self.edit_in_group_by_index(0, group_name, contact)

    def edit_in_group_by_index(self, index, group_name, contact):
        wd = self.gen.wd
        self.open_edit(index, group_name)
        self.enter_contact_parameters(contact)
        wd.find_element_by_name("update").click()
        self.return_to_homepage()
        self.contact_cache = None

    def edit_in_group_by_id(self, id, group_id, contact):
        wd = self.gen.wd
        self.open_edit_by_id(id, group_id)
        self.enter_contact_parameters(contact)
        wd.find_element_by_name("update").click()
        self.return_to_homepage()
        self.contact_cache = None

    def add_all_to_group(self, group_name):
        wd = self.gen.wd
        self.open_home_page()
        wd.find_element_by_xpath("(//input[@id='MassCB'])").click()
        self.select_from_list("to_group", group_name)
        wd.find_element_by_name("add").click()
        wd.find_element_by_link_text('group page "%s"' % group_name).click()
        self.contact_cache = None

    def add_all_to_group_using_id(self, group_id):
        wd = self.gen.wd
        self.open_home_page()
        wd.find_element_by_xpath("(//input[@id='MassCB'])").click()
        self.select_from_list_by_id("to_group", group_id)
        wd.find_element_by_name("add").click()
        wd.find_element_by_xpath("//a[@href='./?group=%s']" % group_id).click()
        self.contact_cache = None

    def add_some_to_group_using_id(self, group_id, contact_id):
        wd = self.gen.wd
        self.open_home_page()
        self.select_contact_by_id(contact_id)
        self.select_from_list_by_id("to_group", group_id)
        wd.find_element_by_name("add").click()
        wd.find_element_by_xpath("//a[@href='./?group=%s']" % group_id).click()
        self.contact_cache = None

    def add_to_group_unselected(self, group_name):
        wd = self.gen.wd
        self.open_home_page()
        self.select_from_list("to_group", group_name)
        wd.find_element_by_name("add").click()
        self.contact_cache = None

    def add_to_group_unselected_using_id(self, group_id):
        wd = self.gen.wd
        self.open_home_page()
        self.select_from_list_by_id("to_group", group_id)
        wd.find_element_by_name("add").click()
        self.contact_cache = None

    def add_to_group_from_another(self, group_from, group_to):
        wd = self.gen.wd
        self.open_contact_group(group_from)
        wd.find_element_by_xpath("(//input[@id='MassCB'])").click()
        self.select_from_list("to_group", group_to)
        wd.find_element_by_name("add").click()
        wd.find_element_by_link_text('group page "%s"' % group_to).click()
        self.contact_cache = None

    def add_to_group_from_another_using_id(self, id_from, id_to):
        wd = self.gen.wd
        self.open_contact_group(id_from)
        wd.find_element_by_xpath("(//input[@id='MassCB'])").click()
        self.select_from_list_by_id("to_group", id_to)
        wd.find_element_by_name("add").click()
        wd.find_element_by_xpath("//a[@href='./?group=%s']" % id_to).click()
        self.contact_cache = None

    def add_some_contact_to_group_from_another(self, contact_id, id_from, id_to):
        wd = self.gen.wd
        self.open_contact_group(id_from)
        self.select_contact_by_id(contact_id)
        self.select_from_list_by_id("to_group", id_to)
        wd.find_element_by_name("add").click()
        wd.find_element_by_xpath("//a[@href='./?group=%s']" % id_to).click()
        self.contact_cache = None

    def remove_from_group(self, group_name):
        wd = self.gen.wd
        self.open_contact_group(group_name)
        wd.find_element_by_xpath("(//input[@id='MassCB'])").click()
        wd.find_element_by_name("remove").click()
        wd.find_element_by_link_text('group page "%s"' % group_name).click()
        self.contact_cache = None

    def remove_all_from_group(self, group_id):
        wd = self.gen.wd
        self.open_contact_group(group_id)
        wd.find_element_by_xpath("(//input[@id='MassCB'])").click()
        wd.find_element_by_name("remove").click()
        wd.find_element_by_xpath("//a[@href='./?group=%s']" % group_id).click()
        self.contact_cache = None

    def remove_some_from_group(self, group_id, contact_id):
        wd = self.gen.wd
        self.open_contact_group(group_id)
        self.select_contact_by_id(contact_id)
        wd.find_element_by_name("remove").click()
        wd.find_element_by_xpath("//a[@href='./?group=%s']" % group_id).click()
        self.contact_cache = None

    def del_all_found(self, search):
        wd = self.gen.wd
        self.open_home_page()
        # find text
        self.set_field_value("searchstring", search)
        # click "select all" & submit deletion
        wd.find_element_by_xpath("(//input[@id='MassCB'])").click()
        wd.find_element_by_xpath("(//input[@value='Delete'])").click()
        wd.switch_to_alert().accept()
        self.wait_close_message_box()
        self.contact_cache = None

    def edit_first_found(self, search, contact):
        wd = self.gen.wd
        # find text & edit contact
        self.open_edit(index=0, search=search)
        self.enter_contact_parameters(contact)
        wd.find_element_by_name("update").click()
        self.return_to_homepage()
        self.contact_cache = None

    def click_first_pencil_img(self, group=None):
        wd = self.gen.wd
        for i in range(self.get_contact_count(group)):
            if wd.find_element_by_xpath("(//img[@alt='Edit'])[%s]" % (i+1)):
                wd.find_element_by_xpath("(//img[@alt='Edit'])[%s]" % (i+1)).click()
                return

    def click_pencil_img(self, index):
        wd = self.gen.wd
        wd.find_elements_by_xpath("(//img[@alt='Edit'])")[index].click()

    def click_pencil_by_id(self, id):
        wd = self.gen.wd
        wd.find_element_by_xpath("//a[@href='edit.php?id=%s']" % id).click()

    contact_cache = None

    def get_contact_list(self, group_id=None, search=None):
        if self.contact_cache is None:
            wd = self.gen.wd
            if group_id is not None:
                self.open_contact_group(group_id)
            else:
                self.open_home_page()
            if search is not None:
                self.set_field_value("searchstring", search)
            self.contact_cache = []
            for i in wd.find_elements_by_name("entry"):
                id = i.find_element_by_name("selected[]").get_attribute('value')
                cells = i.find_elements_by_tag_name("td")
                last_name = cells[1].text
                first_name = cells[2].text
                all_phones = cells[5].text
                all_emails = cells[4].text
                address = cells[3].text
                self.contact_cache.append(Contact(id=id, last_name=last_name, first_name=first_name,
                                                  all_phones=all_phones, all_email=all_emails, address=address))
        return list(self.contact_cache)

    def get_info_from_edit(self, index):
        wd = self.gen.wd
        self.open_edit(index)
        firstname = wd.find_element_by_name('firstname').get_attribute('value')
        lastname = wd.find_element_by_name('lastname').get_attribute('value')
        id = wd.find_element_by_name('id').get_attribute('value')
        home = wd.find_element_by_name('home').get_attribute('value')
        mobile = wd.find_element_by_name('mobile').get_attribute('value')
        work = wd.find_element_by_name('work').get_attribute('value')
        phone2 = wd.find_element_by_name('phone2').get_attribute('value')
        email = wd.find_element_by_name('email').get_attribute('value')
        email2 = wd.find_element_by_name('email2').get_attribute('value')
        email3 = wd.find_element_by_name('email3').get_attribute('value')
        address = wd.find_element_by_name('address').get_attribute('value')
        return Contact(id=id, last_name=lastname, first_name=firstname, home_phone=home, mobile_phone=mobile,
                       work_phone=work, secondary_home_phone=phone2, primary_email=email, secondary_email=email2,
                       third_email=email3, address=address)

    def get_info_from_details(self, index):
        wd = self.gen.wd
        self.open_details(index)
        text = wd.find_element_by_id("content").text
        home = re.search("H: (.*)", text).group(1)
        mobile = re.search("M: (.*)", text).group(1)
        work = re.search("W: (.*)", text).group(1)
        phone = re.search("P: (.*)", text).group(1)
        return Contact(home_phone=home, mobile_phone=mobile,
                       work_phone=work, secondary_home_phone=phone)

