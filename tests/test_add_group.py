# -*- coding: utf-8 -*-
from model.group import Group
import allure


def test_add_group_using_json(gen, db, json_group, check_ui):
    group = json_group
    with allure.step('Given a group list'):
        old_group_list = db.get_group_list()
    with allure.step('When I add the group "%s" to the list' % group):
        gen.group.create(group)
    with allure.step('Then the new group list is equal to the old list with the added group'):
        new_group_list = db.get_group_list()
        old_group_list.append(group)
        assert sorted(old_group_list, key=Group.id_or_max) == sorted(new_group_list, key=Group.id_or_max)
        if check_ui:
            assert sorted(new_group_list, key=Group.id_or_max) == sorted(gen.group.get_group_list(),
                                                                         key=Group.id_or_max)


def test_add_group_using_module(gen, db, data_groups, check_ui):
    group = data_groups
    with allure.step('Given a group list'):
        old_group_list = db.get_group_list()
    with allure.step('When I add the group "%s" to the list' % group):
        gen.group.create(group)
    with allure.step('Then the new group list is equal to the old list with the added group'):
        new_group_list = db.get_group_list()
        old_group_list.append(group)
        assert sorted(old_group_list, key=Group.id_or_max) == sorted(new_group_list, key=Group.id_or_max)
        if check_ui:
            assert sorted(new_group_list, key=Group.id_or_max) == sorted(gen.group.get_group_list(),
                                                                         key=Group.id_or_max)


def test_add_group_with_whitespace(gen, db, check_ui):
    with allure.step('Given a group list'):
        old_group_list = db.get_group_list()
    group = Group(name="name  E7zwRa ", header="header_groupISZ", footer="footer1S tph")
    with allure.step('When I add the group "%s" to the list' % group):
        gen.group.create(group)
    with allure.step('Then the new group list is equal to the old list with the added group'):
        new_group_list = db.get_group_list()
        old_group_list.append(group)
        assert sorted(old_group_list, key=Group.id_or_max) == sorted(new_group_list, key=Group.id_or_max)
        if check_ui:
            assert sorted(new_group_list, key=Group.id_or_max) == sorted(gen.group.get_group_list(),
                                                                         key=Group.id_or_max)


def test_add_empty_v2(gen, db, check_ui):
    with allure.step('Given a group list'):
        old_group_list = db.get_group_list()
    with allure.step('When I add empty group to the list'):
        gen.group.create_empty()
    with allure.step('Then the new group list is equal to the old list with the added group'):
        new_group_list = db.get_group_list()
        old_group_list.append(Group(name=""))
        assert sorted(old_group_list, key=Group.id_or_max) == sorted(new_group_list, key=Group.id_or_max)
        if check_ui:
            assert sorted(new_group_list, key=Group.id_or_max) == sorted(gen.group.get_group_list(),
                                                                         key=Group.id_or_max)
