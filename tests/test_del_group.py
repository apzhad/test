from model.group import Group
import random
import allure


def test_del_first_group(gen, db, check_ui):
    with allure.step('Given a non-empty group list'):
        if len(db.get_group_list()) == 0:
            gen.group.create(Group(name="for_del"))
        old_group_list = db.get_group_list(sorted=True)
    with allure.step('When I delete the first group "%s" from the list' % old_group_list[0].name):
        gen.group.del_first()
    with allure.step('Then the new group list is equal to the old group list without the deleted group'):
        assert len(old_group_list) - 1 == len(db.get_group_list())
        new_group_list = db.get_group_list()
        old_group_list[0:1] = []
        assert sorted(old_group_list, key=Group.id_or_max) == sorted(new_group_list, key=Group.id_or_max)
        if check_ui:
            assert sorted(new_group_list, key=Group.id_or_max) == sorted(gen.group.get_group_list(),
                                                                         key=Group.id_or_max)


def test_del_all_group(gen, db, check_ui):
    with allure.step('Given a non-empty group list'):
        if len(db.get_group_list()) == 0:
            gen.group.create(Group(name="for_del_1"))
            gen.group.create(Group(name="for_del_2"))
            gen.group.create(Group(name="for_del_3"))
    with allure.step('When I delete all groups from the list'):
        gen.group.del_all()
    with allure.step('Then the new group list is empty'):
        new_group_list = db.get_group_list()
        assert [] == new_group_list
        if check_ui:
            assert sorted(new_group_list, key=Group.id_or_max) == sorted(gen.group.get_group_list(),
                                                                         key=Group.id_or_max)


def test_del_last_group(gen, db, check_ui):
    with allure.step('Given a non-empty group list'):
        if len(db.get_group_list()) == 0:
            gen.group.create(Group(name="for_del_1"))
            gen.group.create(Group(name="for_del_2"))
            gen.group.create(Group(name="for_del_3"))
        old_group_list = db.get_group_list(sorted=True)
    with allure.step('When I delete the last group "%s" from the list' % old_group_list[-1].name):
        gen.group.del_last()
    with allure.step('Then the new group list is equal to the old group list without the deleted group'):
        assert len(old_group_list) - 1 == len(db.get_group_list())
        new_group_list = db.get_group_list()
        old_group_list[-1:] = []
        assert sorted(old_group_list, key=Group.id_or_max) == sorted(new_group_list, key=Group.id_or_max)
        if check_ui:
            assert sorted(new_group_list, key=Group.id_or_max) == sorted(gen.group.get_group_list(),
                                                                         key=Group.id_or_max)


def test_del_without_choice_group(gen, db, check_ui):
    with allure.step('Given a non-empty group list'):
        if len(db.get_group_list()) == 0:
            gen.group.create(Group(name="for_del_1"))
            gen.group.create(Group(name="for_del_2"))
        old_group_list = db.get_group_list()
    with allure.step('When I click on delete button without chosen group'):
        gen.group.del_not_choose()
    with allure.step('Then the new group list is equal to the old group list'):
        new_group_list = db.get_group_list()
        assert sorted(old_group_list, key=Group.id_or_max) == sorted(new_group_list, key=Group.id_or_max)
        if check_ui:
            assert sorted(new_group_list, key=Group.id_or_max) == sorted(gen.group.get_group_list(), key=Group.id_or_max)


def test_del_some_group(gen, db, check_ui):
    with allure.step('Given a non-empty group list'):
        if len(db.get_group_list()) == 0:
            gen.group.create(Group(name="for_del"))
        old_group_list = db.get_group_list()
    with allure.step('Given a random group from the list'):
        group = random.choice(old_group_list)
    with allure.step('When I delete the group "%s" from the list' % group.name):
        gen.group.del_by_id(group.id)
    with allure.step('Then the new group list is equal to the old group list without the deleted group'):
        new_group_list = db.get_group_list()
        assert len(old_group_list) - 1 == len(new_group_list)
        old_group_list.remove(group)
        assert sorted(old_group_list, key=Group.id_or_max) == sorted(new_group_list, key=Group.id_or_max)
        if check_ui:
            assert sorted(new_group_list, key=Group.id_or_max) == sorted(gen.group.get_group_list(),
                                                                         key=Group.id_or_max)
