# -*- coding: utf-8 -*-

from model.group import Group


class GroupManage:

    def __init__(self, gen):
        self.gen = gen

    def open_groups_page(self):
        wd = self.gen.wd
        if not (wd.current_url.endswith("/group.php") and len(wd.find_elements_by_name("new")) > 0):
            wd.find_element_by_link_text("groups").click()
        wd.find_element_by_name("new")

    def return_to_groups_page(self):
        wd = self.gen.wd
        wd.find_element_by_link_text("group page").click()
        wd.find_element_by_name("new")

    def create(self, group):
        wd = self.gen.wd
        self.open_groups_page()
        # init new group creation
        wd.find_element_by_name("new").click()
        # enter groups parameters
        self.enter_group_parameters(group)
        # submit group creation and return to group page
        wd.find_element_by_name("submit").click()
        self.return_to_groups_page()
        self.group_cache = None

    def enter_group_parameters(self, group):
        self.set_field_value("group_name", group.name)
        self.set_field_value("group_header", group.header)
        self.set_field_value("group_footer", group.footer)

    def set_field_value(self, field_name, text):
        wd = self.gen.wd
        if text is not None:
            wd.find_element_by_name(field_name).click()
            wd.find_element_by_name(field_name).clear()
            wd.find_element_by_name(field_name).send_keys(text)

    def del_first(self):
        self.del_by_index(0)

    def del_by_index(self, index):
        wd = self.gen.wd
        self.open_groups_page()
        # select group & submit deletion
        self.select_group_by_index(index)
        wd.find_element_by_name("delete").click()
        self.return_to_groups_page()
        self.group_cache = None

    def del_by_id(self, id):
        wd = self.gen.wd
        self.open_groups_page()
        # select group & submit deletion
        self.select_group_by_id(id)
        wd.find_element_by_name("delete").click()
        self.return_to_groups_page()
        self.group_cache = None

    def select_first_group(self):
        wd = self.gen.wd
        wd.find_element_by_name("selected[]").click()

    def select_group_by_index(self, index):
        wd = self.gen.wd
        wd.find_elements_by_name("selected[]")[index].click()

    def select_group_by_id(self, id):
        wd = self.gen.wd
        wd.find_element_by_css_selector("input[value='%s']" % id).click()

    def edit_first(self, group):
        self.edit_by_index(0, group)

    def edit_by_index(self, index, group):
        wd = self.gen.wd
        self.open_groups_page()
        # select group & init editing
        self.select_group_by_index(index)
        wd.find_element_by_name("edit").click()
        # change group parameters
        self.enter_group_parameters(group)
        wd.find_element_by_name("update").click()
        self.return_to_groups_page()
        self.group_cache = None

    def edit_by_id(self, id, group):
        wd = self.gen.wd
        self.open_groups_page()
        # select group & init editing
        self.select_group_by_id(id)
        wd.find_element_by_name("edit").click()
        # change group parameters
        self.enter_group_parameters(group)
        wd.find_element_by_name("update").click()
        self.return_to_groups_page()
        self.group_cache = None

    def update_first_wo_change(self):
        self.update_wo_change_by_index(0)

    def update_wo_change_by_index(self, index):
        wd = self.gen.wd
        self.open_groups_page()
        # select group & init editing
        self.select_group_by_index(index)
        wd.find_element_by_name("edit").click()
        wd.find_element_by_name("update").click()
        self.return_to_groups_page()
        self.group_cache = None

    def update_wo_change_by_id(self, id):
        wd = self.gen.wd
        self.open_groups_page()
        # select group & init editing
        self.select_group_by_id(id)
        wd.find_element_by_name("edit").click()
        wd.find_element_by_name("update").click()
        self.return_to_groups_page()
        self.group_cache = None

    def del_all(self):
        wd = self.gen.wd
        self.open_groups_page()
        self.select_all_groups()
        wd.find_element_by_name("delete").click()
        self.return_to_groups_page()
        self.group_cache = None

    def select_all_groups(self):
        wd = self.gen.wd
        # get group count
        group_count = self.get_group_count()
        # select all groups
        for i in range(group_count):
            wd.find_element_by_xpath("(//input[@name='selected[]'])[%s]" % (i + 1)).click()

    def get_group_count(self):
        wd = self.gen.wd
        self.open_groups_page()
        return len(wd.find_elements_by_name("selected[]"))

    group_cache = None

    def get_group_list(self):
        if self.group_cache is None:
            wd = self.gen.wd
            self.open_groups_page()
            self.group_cache = []
            for i in wd.find_elements_by_css_selector("span.group"):
                text = i.text
                id = i.find_element_by_name("selected[]").get_attribute('value')
                self.group_cache.append(Group(name=text, id=id))
        return list(self.group_cache)

    def get_groups_names(self):
        group_list = self.get_group_list()
        group_name = []
        for i in range(len(group_list)):
            group_name.append(group_list[i].name)
        return list(group_name)

    def del_last(self):
        self.del_by_index(self.get_group_count()-1)

    def del_not_choose(self):
        wd = self.gen.wd
        self.open_groups_page()
        wd.find_element_by_name("delete").click()
        self.return_to_groups_page()
        self.group_cache = None

    def create_empty(self):
        wd = self.gen.wd
        self.open_groups_page()
        # init new group creation
        wd.find_element_by_name("new").click()
        # submit group creation and return to group page
        wd.find_element_by_name("submit").click()
        self.return_to_groups_page()
        self.group_cache = None

    def edit_all(self, group):
        wd = self.gen.wd
        self.open_groups_page()
        self.select_all_groups()
        wd.find_element_by_name("edit").click()
        # change group parameters
        self.enter_group_parameters(group)
        wd.find_element_by_name("update").click()
        self.return_to_groups_page()
        self.group_cache = None

    def edit_all_wo_change(self):
        wd = self.gen.wd
        self.open_groups_page()
        self.select_all_groups()
        wd.find_element_by_name("edit").click()
        wd.find_element_by_name("update").click()
        self.return_to_groups_page()
        self.group_cache = None

    def edit_last(self, group):
        self.edit_by_index((self.get_group_count() - 1), group)

    def select_last_group(self):
        wd = self.gen.wd
        group_count = self.get_group_count()
        wd.find_element_by_xpath("(//input[@name='selected[]'])[%s]" % group_count).click()

    def update_last_wo_change(self):
        self.update_wo_change_by_index(self.get_group_count() - 1)
