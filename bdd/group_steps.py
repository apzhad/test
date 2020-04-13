from pytest_bdd import given, when, then
from model.group import Group
import random


@given("a group list")
def group_list(db):
    return db.get_group_list()


@given("a group with <name>, <header> and <footer>")
def new_group(name, header, footer):
    return Group(name=name, header=header, footer=footer)


@when("I add the group to the list")
def add_new_group(gen, new_group):
    gen.group.create(new_group)


@then("the new group list is equal to the old list with the added group")
def verify_group_added(db, group_list, new_group):
    old_group_list = group_list
    new_group_list = db.get_group_list()
    old_group_list.append(new_group)
    assert sorted(old_group_list, key=Group.id_or_max) == sorted(new_group_list, key=Group.id_or_max)


@given('a non-empty group list')
def non_empty_group_list(db, gen):
    if len(db.get_group_list()) == 0:
        gen.group.create(Group(name='some name'))
    return db.get_group_list()


@given('a random group from the list')
def random_group(non_empty_group_list):
    return random.choice(non_empty_group_list)


@when('I delete the group from the list')
def delete_group(gen, random_group):
    gen.group.del_by_id(random_group.id)


@then('the new group list is equal to the old group list without the deleted group')
def verify_group_deleted(db, non_empty_group_list, random_group, gen, check_ui):
    old_group_list = non_empty_group_list
    new_group_list = db.get_group_list()
    assert len(old_group_list)-1 == len(new_group_list)
    old_group_list.remove(random_group)
    assert sorted(old_group_list, key=Group.id_or_max) == sorted(new_group_list, key=Group.id_or_max)
    if check_ui:
        assert sorted(new_group_list, key=Group.id_or_max) == sorted(gen.group.get_group_list(), key=Group.id_or_max)
