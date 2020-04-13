import re
from model.contact import Contact
import allure


def test_info_on_homepage(gen, orm):
    with allure.step('Given contact list from database'):
        info_in_db = sorted(orm.get_contact_list(), key=Contact.id_or_max)
    with allure.step('Given contact list from homepage'):
        info_on_homepage = sorted(gen.contact.get_contact_list(), key=Contact.id_or_max)
    with allure.step('Then both contact lists and info are equal'):
        assert len(info_in_db) == len(info_on_homepage)
        for i in range(len(info_on_homepage)):
            assert info_on_homepage[i].first_name == info_in_db[i].first_name
            assert info_on_homepage[i].last_name == info_in_db[i].last_name
            assert info_on_homepage[i].address == info_in_db[i].address
            assert info_on_homepage[i].all_email == merge_email(info_in_db[i])
            assert info_on_homepage[i].all_phones == merge_phone(info_in_db[i])


"""
def test_info_in_details(gen):
    #index = randrange(len(gen.contact.get_contact_list()))
    for index in range(len(gen.contact.get_contact_list())):
        info_from_details = gen.contact.get_info_from_details(index)
        info_from_edit = gen.contact.get_info_from_edit(index)
    #assert info_from_details.first_name == info_from_edit.first_name
    #assert info_from_details.last_name == info_from_edit.last_name
    #assert info_from_details.address == info_from_edit.address
    #assert info_from_details.all_email == merge_email(info_from_edit)
        assert merge_phone(info_from_details) == merge_phone(info_from_edit)
"""


def clear_spec_symbol(s):
    return re.sub("[() -]", "", s)


def merge_phone(contact):
    return "\n".join(filter(lambda x: x != "",
                            map(lambda x: clear_spec_symbol(x),
                                filter(lambda x: x is not None,
                                       [contact.home_phone, contact.mobile_phone,
                                        contact.work_phone, contact.secondary_home_phone]))))


def merge_email(contact):
    return "\n".join(filter(lambda x: x != "",
                            filter(lambda x: x is not None,
                                   [contact.primary_email, contact.secondary_email, contact.third_email])))
