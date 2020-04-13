from model.group import Group
import random
import allure


def find_index(group, id):
    index = 0
    for gr in group:
        if gr.id == id:
            break
        index += 1
    return index


def test_edit_first_group(gen, db, check_ui):
    with allure.step('Given a non-empty group list'):
        if len(db.get_group_list()) == 0:
            gen.group.create(Group(name="for_edit"))
        old_group_list = db.get_group_list(sorted=True)
    with allure.step('Given data for modify'):
        group = Group(name="new_name", header="new_header_group", footer="changed_group")
    group.id = old_group_list[0].id
    with allure.step('When I modify the first group "%s" from the list' % old_group_list[0].name):
        gen.group.edit_first(group)
    with allure.step('Then the new group list is equal to the old group list with the modified group'):
        assert len(old_group_list) == len(db.get_group_list())
        new_group_list = db.get_group_list()
        old_group_list[0] = group
        assert sorted(old_group_list, key=Group.id_or_max) == sorted(new_group_list, key=Group.id_or_max)
        if check_ui:
            assert sorted(new_group_list, key=Group.id_or_max) == sorted(gen.group.get_group_list(), key=Group.id_or_max)


def test_edit_some_group(gen, db, check_ui):
    with allure.step('Given a non-empty group list'):
        if len(db.get_group_list()) == 0:
            gen.group.create(Group(name="for_edit"))
        old_group_list = db.get_group_list()
    with allure.step('Given a random group from the list'):
        group = random.choice(old_group_list)
    gid = group.id
    index = find_index(group=old_group_list, id=gid)
    with allure.step('Given data for modify'):
        group = Group(id=gid, name="edit_some", header="group")
    with allure.step('When I modify the group "%s" from the list' % group.name):
        gen.group.edit_by_id(gid, group)
    with allure.step('Then the new group list is equal to the old group list with the modified group'):
        assert len(old_group_list) == len(db.get_group_list())
        new_group_list = db.get_group_list()
        old_group_list[index] = group
        assert sorted(old_group_list, key=Group.id_or_max) == sorted(new_group_list, key=Group.id_or_max)
        if check_ui:
            assert sorted(new_group_list, key=Group.id_or_max) == sorted(gen.group.get_group_list(), key=Group.id_or_max)


def test_clear_first_group_params(gen, db, check_ui):
    with allure.step('Given a non-empty group list'):
        if len(db.get_group_list()) == 0:
            gen.group.create(Group(name="for_edit", header="header", footer="footer"))
        old_group_list = db.get_group_list(sorted=True)
    group = Group(name="", header="", footer="")
    group.id = old_group_list[0].id
    with allure.step('When I clear parameters of the first group "%s" in the list' % group.name):
        gen.group.edit_first(group)
    with allure.step('Then the new group list is equal to the old group list with the modified group'):
        assert len(old_group_list) == len(db.get_group_list())
        new_group_list = db.get_group_list()
        old_group_list[0] = group
        assert sorted(old_group_list, key=Group.id_or_max) == sorted(new_group_list, key=Group.id_or_max)
        if check_ui:
            assert sorted(new_group_list, key=Group.id_or_max) == sorted(gen.group.get_group_list(), key=Group.id_or_max)


def test_clear_some_group_params(gen, db, check_ui):
    with allure.step('Given a non-empty group list'):
        if len(db.get_group_list()) == 0:
            gen.group.create(Group(name="for_edit", header="header", footer="footer"))
        old_group_list = db.get_group_list()
    with allure.step('Given a random group from the list'):
        group = random.choice(old_group_list)
    gid = group.id
    group = Group(id=gid, name="", header="", footer="")
    index = find_index(old_group_list, gid)
    with allure.step('When I clear parameters of the group "%s" in the list' % group.name):
        gen.group.edit_by_id(id=gid, group=group)
    with allure.step('Then the new group list is equal to the old group list with the modified group'):
        assert len(old_group_list) == len(db.get_group_list())
        new_group_list = db.get_group_list()
        old_group_list[index] = group
        assert sorted(old_group_list, key=Group.id_or_max) == sorted(new_group_list, key=Group.id_or_max)
        if check_ui:
            assert sorted(new_group_list, key=Group.id_or_max) == sorted(gen.group.get_group_list(), key=Group.id_or_max)


def test_update_first_group_without_changes(gen, db, check_ui):
    with allure.step('Given a non-empty group list'):
        if len(db.get_group_list()) == 0:
            gen.group.create(Group(name="for_edit", header="header", footer="footer"))
        old_group_list = db.get_group_list()
    with allure.step('When I modify the first group "%s" from the list without changes' % old_group_list[0].name):
        gen.group.update_first_wo_change()
    with allure.step('Then the new group list is equal to the old group list'):
        assert len(old_group_list) == len(db.get_group_list())
        new_group_list = db.get_group_list()
        assert sorted(old_group_list, key=Group.id_or_max) == sorted(new_group_list, key=Group.id_or_max)
        if check_ui:
            assert sorted(new_group_list, key=Group.id_or_max) == sorted(gen.group.get_group_list(), key=Group.id_or_max)


def test_update_some_group_without_changes(gen, db, check_ui):
    with allure.step('Given a non-empty group list'):
        if len(db.get_group_list()) == 0:
            gen.group.create(Group(name="for_edit", header="header", footer="footer"))
        old_group_list = db.get_group_list()
    with allure.step('Given a random group from the list'):
        group = random.choice(old_group_list)
    with allure.step('When I modify the group "%s" from the list without changes' % group.name):
        gen.group.update_wo_change_by_id(group.id)
    with allure.step('Then the new group list is equal to the old group list'):
        assert len(old_group_list) == len(db.get_group_list())
        new_group_list = db.get_group_list()
        assert sorted(old_group_list, key=Group.id_or_max) == sorted(new_group_list, key=Group.id_or_max)
        if check_ui:
            assert sorted(new_group_list, key=Group.id_or_max) == sorted(gen.group.get_group_list(), key=Group.id_or_max)


def test_update_all_groups(gen, db, check_ui):
    with allure.step('Given a non-empty group list'):
        if len(db.get_group_list()) == 0:
            gen.group.create(Group(name="for_edit", header="header", footer="footer"))
            gen.group.create(Group(name="for_edit_1", header="header_1", footer="footer_1"))
            gen.group.create(Group(name="for_edit_2", header="header_2", footer="footer_2"))
        old_group_list = db.get_group_list(sorted=True)
    with allure.step('Given data for modify'):
        group = Group(name="some_name", header="some_header_group", footer="changed_group")
    group.id = old_group_list[0].id
    with allure.step('When I choose all groups in the list and modify them'):
        gen.group.edit_all(group)
    with allure.step('Then the new group list is equal to the old group list with modified first group in the old list'):
        assert len(old_group_list) == len(db.get_group_list())
        new_group_list = db.get_group_list()
        old_group_list[0] = group
        assert sorted(old_group_list, key=Group.id_or_max) == sorted(new_group_list, key=Group.id_or_max)
        if check_ui:
            assert sorted(new_group_list, key=Group.id_or_max) == sorted(gen.group.get_group_list(),
                                                                         key=Group.id_or_max)


def test_update_all_groups_without_changes(gen, db, check_ui):
    with allure.step('Given a non-empty group list'):
        if len(db.get_group_list()) == 0:
            gen.group.create(Group(name="for_edit", header="header", footer="footer"))
            gen.group.create(Group(name="for_edit_1", header="header_1", footer="footer_1"))
            gen.group.create(Group(name="for_edit_2", header="header_2", footer="footer_2"))
        old_group_list = db.get_group_list()
    with allure.step('When I choose all groups in the list and modify them without changes'):
        gen.group.edit_all_wo_change()
    with allure.step('Then the new group list is equal to the old group list'):
        assert len(old_group_list) == len(db.get_group_list())
        new_group_list = db.get_group_list()
        assert sorted(old_group_list, key=Group.id_or_max) == sorted(new_group_list, key=Group.id_or_max)
        if check_ui:
            assert sorted(new_group_list, key=Group.id_or_max) == sorted(gen.group.get_group_list(),
                                                                         key=Group.id_or_max)


def test_update_last_group(gen, db, check_ui):
    with allure.step('Given a non-empty group list'):
        if len(db.get_group_list()) == 0:
            gen.group.create(Group(name="for_edit", header="header", footer="footer"))
            gen.group.create(Group(name="for_edit_1", header="header_1", footer="footer_1"))
        old_group_list = db.get_group_list(sorted=True)
    with allure.step('Given data for modify'):
        group = Group(name="last_name", header="last_header_group", footer="last_group")
    group.id = old_group_list[-1].id
    with allure.step('When I modify the last group "%s" from the list' % old_group_list[-1].name):
        gen.group.edit_last(group)
    with allure.step('Then the new group list is equal to the old group list with the modified group'):
        assert len(old_group_list) == len(db.get_group_list())
        new_group_list = db.get_group_list()
        old_group_list[-1] = group
        assert sorted(old_group_list, key=Group.id_or_max) == sorted(new_group_list, key=Group.id_or_max)
        if check_ui:
            assert sorted(new_group_list, key=Group.id_or_max) == sorted(gen.group.get_group_list(),
                                                                         key=Group.id_or_max)


def test_update_last_group_without_changes(gen, db, check_ui):
    with allure.step('Given a non-empty group list'):
        if len(db.get_group_list()) == 0:
            gen.group.create(Group(name="for_edit", header="header", footer="footer"))
            gen.group.create(Group(name="for_edit_1", header="header_1", footer="footer_1"))
        old_group_list = db.get_group_list(sorted=True)
    with allure.step('When I modify the last group "%s" from the list without changes' % old_group_list[-1].name):
        gen.group.update_last_wo_change()
    with allure.step('Then the new group list is equal to the old group list'):
        assert len(old_group_list) == len(db.get_group_list())
        new_group_list = db.get_group_list()
        assert sorted(old_group_list, key=Group.id_or_max) == sorted(new_group_list, key=Group.id_or_max)
        if check_ui:
            assert sorted(new_group_list, key=Group.id_or_max) == sorted(gen.group.get_group_list(),
                                                                         key=Group.id_or_max)


def test_edit_first_group_name(gen, db, check_ui):
    with allure.step('Given a non-empty group list'):
        if len(db.get_group_list()) == 0:
            gen.group.create(Group(name="for_edit", header="header", footer="footer"))
        old_group_list = db.get_group_list(sorted=True)
    with allure.step('Given name for modify'):
        group = Group(name="only_name")
    group.id = old_group_list[0].id
    with allure.step('When I modify name of the first group "%s" in the list' % old_group_list[0].name):
        gen.group.edit_first(group)
    with allure.step('Then the new group list is equal to the old group list with the modified group'):
        assert len(old_group_list) == len(db.get_group_list())
        new_group_list = db.get_group_list()
        old_group_list[0] = group
        assert sorted(old_group_list, key=Group.id_or_max) == sorted(new_group_list, key=Group.id_or_max)
        if check_ui:
            assert sorted(new_group_list, key=Group.id_or_max) == sorted(gen.group.get_group_list(),
                                                                         key=Group.id_or_max)


def test_edit_some_group_name(gen, db, check_ui):
    with allure.step('Given a non-empty group list'):
        if len(db.get_group_list()) == 0:
            gen.group.create(Group(name="for_edit", header="header", footer="footer"))
        old_group_list = db.get_group_list()
    with allure.step('Given a random group from the list'):
        group = random.choice(old_group_list)
    gid = group.id
    with allure.step('Given name for modify'):
        group = Group(id=gid, name="only_name")
    index = find_index(old_group_list, gid)
    with allure.step('When I modify name of the group "%s" in the list' % group.name):
        gen.group.edit_by_id(gid, group)
    with allure.step('Then the new group list is equal to the old group list with the modified group'):
        assert len(old_group_list) == len(db.get_group_list())
        new_group_list = db.get_group_list()
        old_group_list[index] = group
        assert sorted(old_group_list, key=Group.id_or_max) == sorted(new_group_list, key=Group.id_or_max)
        if check_ui:
            assert sorted(new_group_list, key=Group.id_or_max) == sorted(gen.group.get_group_list(),
                                                                         key=Group.id_or_max)
