from pytest_bdd import scenario
from .contact_steps import *


@scenario('contact.feature', 'Add new contact')
def test_add_new_contact():
    pass


@scenario('contact.feature', 'Modify contact')
def test_modify_contact():
    pass


@scenario('contact.feature', 'Delete contact')
def test_delete_contact():
    pass


@scenario('contact.feature', 'Cancel delete contact')
def test_calcel_delete_contact():
    pass


@scenario('contact.feature', 'Delete all contacts')
def test_delete_all_contact():
    pass


@scenario('contact.feature', 'Modify contact from detail')
def test_modify_contact_from_detail():
    pass
