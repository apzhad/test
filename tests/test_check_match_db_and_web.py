from model.group import Group
from model.contact import Contact
import allure


def test_group_list(gen, db):
    with allure.step('Given group list from group page'):
        web_group = gen.group.get_group_list()
    with allure.step('Given group list from database'):
        db_group = db.get_group_list()
    with allure.step('Then both group lists are equal'):
        assert sorted(web_group, key=Group.id_or_max) == sorted(db_group, key=Group.id_or_max)


def test_contact_list(gen, db):
    with allure.step('Given contact list from homepage'):
        web_contact = gen.contact.get_contact_list()
    with allure.step('Given contact list from database'):
        db_contact = db.get_contact_list()
    with allure.step('Then both contact lists are equal'):
        assert sorted(web_contact, key=Contact.id_or_max) == sorted(db_contact, key=Contact.id_or_max)
