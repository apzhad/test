# -*- coding: utf-8 -*-
from model.contact import Contact
from model.group import Group
import random
import allure


month = ("January", "February", "March", "April", "May", "June", "July",
         "August", "September", "October", "November", "December")


def test_add_contact_using_json(gen, db, json_contact, check_ui):
    contact = json_contact
    with allure.step('Given a contact list'):
        old_contact_list = db.get_contact_list()
    with allure.step('Given a group list and choose a group from it'):
        group = db.get_group_list()
        group.append(Group(id="[none]", name="[none]"))
        group = random.choice(group)
        contact.group_name = group.id
    with allure.step('When I add the contact "%s" to the list and into the group "%s"' % (contact, group.name)):
        gen.contact.create(contact)
    with allure.step('Then the new contact list is equal to the old list with the added contact'):
        assert len(old_contact_list) + 1 == len(db.get_contact_list())
        new_contact_list = db.get_contact_list()
        old_contact_list.append(contact)
        assert sorted(old_contact_list, key=Contact.id_or_max) == sorted(new_contact_list, key=Contact.id_or_max)
        if check_ui:
            assert sorted(new_contact_list, key=Contact.id_or_max) == sorted(gen.contact.get_contact_list(),
                                                                             key=Contact.id_or_max)


def test_add_contact_using_module(gen, data_contacts, check_ui, db):
    contact = data_contacts
    with allure.step('Given a contact list'):
        old_contact_list = db.get_contact_list()
    with allure.step('Given a group list and choose a group from it'):
        group = db.get_group_list()
        group.append(Group(id="[none]", name="[none]"))
        group = random.choice(group)
        contact.group_name = group.id
    with allure.step('When I add the contact "%s" to the list and into the group "%s"' % (contact, group.name)):
        gen.contact.create(contact)
    with allure.step('Then the new contact list is equal to the old list with the added contact'):
        assert len(old_contact_list) + 1 == len(db.get_contact_list())
        new_contact_list = db.get_contact_list()
        old_contact_list.append(contact)
        assert sorted(old_contact_list, key=Contact.id_or_max) == sorted(new_contact_list, key=Contact.id_or_max)
        if check_ui:
            assert sorted(new_contact_list, key=Contact.id_or_max) == sorted(gen.contact.get_contact_list(),
                                                                             key=Contact.id_or_max)


def test_add_contact_into_group(gen, db, check_ui):
    with allure.step('Given a contact list'):
        old_contact_list = db.get_contact_list()
    with allure.step('Given a contact to add'):
        cont = Contact(first_name="first_name ", middle_name="middle_name", last_name="last_name", nickname="nickname",
                       title="title", company="company", address="address", home_phone="homephone",
                       mobile_phone="mobilephone", work_phone="workphone", fax="fax", primary_email="email",
                       secondary_email="email2", third_email="email3", homepage="homepage", birth_day="1",
                       birth_month=random.choice(month), birth_year="1950", anniversary_day="15",
                       anniversary_month="June", anniversary_year="2000", secondary_address="address secondary",
                       secondary_home_phone="home secondary", notes="notes", photo_path="cat.jpg")
    with allure.step('Given a group list and choose a group from it'):
        group = db.get_group_list()
        group.append(Group(id="[none]", name="[none]"))
        group = random.choice(group)
        cont.group_name = group.id
    with allure.step('When I add the contact "%s" to the list and into the group "%s"' % (cont, group.name)):
        gen.contact.create(cont)
    with allure.step('Then the new contact list is equal to the old list with the added contact'):
        assert len(old_contact_list) + 1 == len(db.get_contact_list())
        new_contact_list = db.get_contact_list()
        old_contact_list.append(cont)
        assert sorted(old_contact_list, key=Contact.id_or_max) == sorted(new_contact_list, key=Contact.id_or_max)
        if check_ui:
            assert sorted(new_contact_list, key=Contact.id_or_max) == sorted(gen.contact.get_contact_list(),
                                                                         key=Contact.id_or_max)


def test_add_empty_contact(gen, db, check_ui):
    with allure.step('Given a contact list'):
        old_contact_list = db.get_contact_list()
    with allure.step('When I add empty contact to the list'):
        gen.contact.create_empty()
    with allure.step('Then the new contact list is equal to the old list with the added contact'):
        assert len(old_contact_list) + 1 == len(db.get_contact_list())
        new_contact_list = db.get_contact_list()
        old_contact_list.append(Contact(first_name="", last_name=""))
        assert sorted(old_contact_list, key=Contact.id_or_max) == sorted(new_contact_list, key=Contact.id_or_max)
        if check_ui:
            assert sorted(new_contact_list, key=Contact.id_or_max) == sorted(gen.contact.get_contact_list(),
                                                                             key=Contact.id_or_max)
