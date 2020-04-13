"""
Библиотека для Robot Framework 3.0
Запуск тестов осуществляется через python -m robot rf
"""

import pytest
from fixture.generic import Generic
from fixture.db import DbFixture
from fixture.orm import ORMFixture
import json
import os.path
from model.group import Group
from model.contact import Contact
import importlib
import jsonpickle


def find_index(contacts, id):
    index = 0
    for c in contacts:
        if c.id == id:
            break
        index += 1
    return index


class Addressbook:

    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'

    def __init__(self, config="settings.json", browser="firefox"):
        self.browser = browser
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", config)
        with open(config_file) as f:
            self.settings = json.load(f)

    def init_fixture(self):
        web_conf = self.settings['web']
        self.fixture = Generic(browser=self.browser, base_url=web_conf["base_url"])
        self.fixture.session.ensure_login(username=web_conf["username"], password=web_conf["password"])
        db_conf = self.settings["db"]
        self.dbfixture = DbFixture(host=db_conf["host"], name=db_conf["name"], user=db_conf["username"],
                                   password=db_conf["password"])

    def finish_fixture(self):
        self.fixture.finish()
        self.dbfixture.finish()

    def get_group_list(self):
        return self.dbfixture.get_group_list()

    def new_group(self, name, header, footer):
        return Group(name=name, header=header, footer=footer)

    def create_group(self, group):
        self.fixture.group.create(group)

    def delete_group(self, group):
        self.fixture.group.del_by_id(group.id)

    def group_lists_should_be_equal(self, list1, list2):
        assert sorted(list1, key=Group.id_or_max) == sorted(list2, key=Group.id_or_max)

    def get_contact_list(self):
        return self.dbfixture.get_contact_list()

    def new_contact(self, first_name, last_name, address, home_phone):
        return Contact(first_name=first_name, last_name=last_name, address=address, home_phone=home_phone)

    def create_contact(self, contact):
        self.fixture.contact.create(contact)

    def contact_lists_should_be_equal(self, list1, list2):
        assert sorted(list1, key=Contact.id_or_max) == sorted(list2, key=Contact.id_or_max)

    def modify_contact(self, contact, modify_data):
        self.fixture.contact.edit_by_id(contact.id, modify_data)
        modify_data.id = contact.id

    def modify_contact_from_detail(self, contact, modify_data):
        self.fixture.contact.edit_from_details_by_id(contact.id, modify_data)
        modify_data.id = contact.id

    def delete_contact(self, contact):
        self.fixture.contact.del_by_id(contact.id)

    def cancel_delete_contact(self, contact):
        self.fixture.contact.cancel_del_by_id(contact.id)

    def delete_all_contacts(self):
        self.fixture.contact.del_by_select_all()

    def contact_list_should_be_empty(self, list):
        assert [] == list

    def check_contact_exist(self):
        if len(self.dbfixture.get_contact_list()) == 0:
            self.fixture.contact.create(Contact(first_name="del_contact", fax="573-092", nickname="1"))
            self.fixture.contact.create(Contact(first_name="del_contact", fax="573-092", nickname="2"))
            self.fixture.contact.create(Contact(first_name="del_contact", fax="573-092", nickname="3"))
