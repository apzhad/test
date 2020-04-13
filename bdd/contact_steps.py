from pytest_bdd import given, when, then
from model.contact import Contact
import random


@given('a contact list')
def contact_list(db):
    return db.get_contact_list()


@given('a contact with <first_name>, <last_name>, <address> and <home_phone>')
def new_contact(first_name, last_name, address, home_phone):
    return Contact(first_name=first_name, last_name=last_name, address=address, home_phone=home_phone)


@when('I add the contact to the list')
def add_contact(gen, new_contact):
    gen.contact.create(new_contact)


@then('the new contact list is equal to the old list with the added contact')
def verify_contact_added(contact_list, db, new_contact, check_ui, gen):
    old_contact_list = contact_list
    new_contact_list = db.get_contact_list()
    assert len(old_contact_list) + 1 == len(db.get_contact_list())
    old_contact_list.append(new_contact)
    assert sorted(old_contact_list, key=Contact.id_or_max) == sorted(new_contact_list, key=Contact.id_or_max)
    if check_ui:
        assert sorted(new_contact_list, key=Contact.id_or_max) == sorted(gen.contact.get_contact_list(),
                                                                         key=Contact.id_or_max)


@given('a non-empty contact list')
def non_empty_contact_list(db, gen):
    if len(db.get_contact_list()) == 0:
        gen.contact.create(Contact(first_name="modify"))
    return db.get_contact_list()


@given('a random contact from the list')
def random_contact(non_empty_contact_list):
    return random.choice(non_empty_contact_list)


@given('a <first_name>, <last_name>, <address> and <home_phone> for modify')
def modify_data(first_name, last_name, address, home_phone):
    return Contact(first_name=first_name, last_name=last_name, address=address, home_phone=home_phone)


@when('I modify the contact from the list')
def modify_contact(gen, modify_data, random_contact):
    gen.contact.edit_by_id(random_contact.id, modify_data)


@then('the new contact list is equal to the old list with modified contact')
def verify_modifed_contact(non_empty_contact_list, db, modify_data, check_ui, gen, random_contact):
    old_contact_list = non_empty_contact_list
    new_contact_list = db.get_contact_list()
    assert len(old_contact_list) == len(new_contact_list)
    index = find_index(old_contact_list, random_contact.id)
    modify_data.id = random_contact.id
    old_contact_list[index] = modify_data
    assert sorted(old_contact_list, key=Contact.id_or_max) == sorted(new_contact_list, key=Contact.id_or_max)
    if check_ui:
        assert sorted(new_contact_list, key=Contact.id_or_max) == sorted(gen.contact.get_contact_list(),
                                                                         key=Contact.id_or_max)


@when('I delete the contact from the list')
def delete_contact(gen, random_contact):
    gen.contact.del_by_id(random_contact.id)


@then('the new contact list is equal to the old list without the deleted contact')
def verify_contact_deleted(non_empty_contact_list, db, random_contact, check_ui, gen):
    old_contact_list = non_empty_contact_list
    cid = int(random_contact.id)
    assert len(old_contact_list) - 1 == len(db.get_contact_list())
    new_contact_list = db.get_contact_list()
    old_contact_list[cid:cid + 1] = []
    assert sorted(new_contact_list, key=Contact.id_or_max) == sorted(new_contact_list, key=Contact.id_or_max)
    if check_ui:
        assert sorted(new_contact_list, key=Contact.id_or_max) == sorted(gen.contact.get_contact_list(),
                                                                         key=Contact.id_or_max)


@when('I delete the contact from the list and cancel deletion')
def cancel_del_contact(gen, random_contact):
    gen.contact.cancel_del_by_id(random_contact.id)


@then('the new contact list is equal to the old list without changes')
def verify_modifed_contact(non_empty_contact_list, db, check_ui, gen):
    old_contact_list = non_empty_contact_list
    assert len(old_contact_list) == len(db.get_contact_list())
    new_contact_list = db.get_contact_list()
    assert sorted(old_contact_list, key=Contact.id_or_max) == sorted(new_contact_list, key=Contact.id_or_max)
    if check_ui:
        assert sorted(new_contact_list, key=Contact.id_or_max) == sorted(gen.contact.get_contact_list(),
                                                                         key=Contact.id_or_max)


@when('I click on "Select all" and then delete contacts')
def delete_all_contact(gen):
    gen.contact.del_by_select_all()


@then('the new contact list is empty')
def verify_empty_list(db, check_ui, gen):
    assert 0 == len(db.get_contact_list())
    new_contact_list = db.get_contact_list()
    assert [] == new_contact_list
    if check_ui:
        assert sorted(new_contact_list, key=Contact.id_or_max) == sorted(gen.contact.get_contact_list(),
                                                                         key=Contact.id_or_max)


@when('I open details and modify the contact from the list')
def open_datails_and_modify(gen, random_contact, modify_data):
    gen.contact.edit_from_details_by_id(random_contact.id, modify_data)


def find_index(contacts, id):
    index = 0
    for c in contacts:
        if c.id == id:
            break
        index += 1
    return index
