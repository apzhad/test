from model.contact import Contact
import random
import allure


def test_del_first_contact(gen, check_ui, db):
    with allure.step('Given a non-empty contact list and sorted by firstname'):
        if len(db.get_contact_list()) == 0:
            gen.contact.create(Contact(first_name="del_contact", fax="573-092", nickname="1"))
        old_contact_list = db.get_contact_list(sorted=True)
    with allure.step('When I delete first contact from the sorted list and accept deletion'):
        gen.contact.del_first()
    with allure.step('Then the new contact list is equal to the old list without the deleted contact'):
        assert len(old_contact_list) - 1 == len(db.get_contact_list())
        new_contact_list = db.get_contact_list()
        old_contact_list[0:1] = []
        assert sorted(new_contact_list, key=Contact.id_or_max) == sorted(new_contact_list, key=Contact.id_or_max)
        if check_ui:
            assert sorted(new_contact_list, key=Contact.id_or_max) == sorted(gen.contact.get_contact_list(),
                                                                         key=Contact.id_or_max)


def test_del_some_contact(gen, db, check_ui):
    with allure.step('Given a non-empty contact list'):
        if len(db.get_contact_list()) == 0:
            gen.contact.create(Contact(first_name="del_contact", fax="573-092", nickname="1"))
        old_contact_list = db.get_contact_list()
    with allure.step('Given a random contact from the list'):
        cid = int(random.choice(old_contact_list).id)
    with allure.step('When I delete the contact from the list and accept deletion'):
        gen.contact.del_by_id(cid)
    with allure.step('Then the new contact list is equal to the old list without the deleted contact'):
        assert len(old_contact_list) - 1 == len(db.get_contact_list())
        new_contact_list = db.get_contact_list()
        old_contact_list[cid:cid+1] = []
        assert sorted(new_contact_list, key=Contact.id_or_max) == sorted(new_contact_list, key=Contact.id_or_max)
        if check_ui:
            assert sorted(new_contact_list, key=Contact.id_or_max) == sorted(gen.contact.get_contact_list(),
                                                                             key=Contact.id_or_max)


def test_cancel_del_first_contact(gen, db, check_ui):
    with allure.step('Given a non-empty contact list'):
        if len(db.get_contact_list()) == 0:
            gen.contact.create(Contact(first_name="del_contact", fax="573-092", nickname="1"))
        old_contact_list = db.get_contact_list()
    with allure.step('When I delete first contact and cancel deletion'):
        gen.contact.cancel_del_first()
    with allure.step('Then the new contact list is equal to the old list without changes'):
        assert len(old_contact_list) == len(db.get_contact_list())
        new_contact_list = db.get_contact_list()
        assert sorted(new_contact_list, key=Contact.id_or_max) == sorted(new_contact_list, key=Contact.id_or_max)
        if check_ui:
            assert sorted(new_contact_list, key=Contact.id_or_max) == sorted(gen.contact.get_contact_list(),
                                                                             key=Contact.id_or_max)


def test_cancel_del_some_contact(gen, db, check_ui):
    with allure.step('Given a non-empty contact list'):
        if len(db.get_contact_list()) == 0:
            gen.contact.create(Contact(first_name="del_contact", fax="573-092", nickname="1"))
        old_contact_list = db.get_contact_list()
    with allure.step('Given a random contact from the list'):
        cid = int(random.choice(old_contact_list).id)
    with allure.step('When I delete the contact from the list and cancel deletion'):
        gen.contact.cancel_del_by_id(cid)
    with allure.step('Then the new contact list is equal to the old list without changes'):
        assert len(old_contact_list) == len(db.get_contact_list())
        new_contact_list = db.get_contact_list()
        assert sorted(new_contact_list, key=Contact.id_or_max) == sorted(new_contact_list, key=Contact.id_or_max)
        if check_ui:
            assert sorted(new_contact_list, key=Contact.id_or_max) == sorted(gen.contact.get_contact_list(),
                                                                             key=Contact.id_or_max)


def test_del_all_contacts_select(gen, db, check_ui):
    with allure.step('Given a non-empty contact list'):
        if len(db.get_contact_list()) == 0:
            gen.contact.create(Contact(first_name="del_contact", fax="573-092", nickname="1"))
            gen.contact.create(Contact(first_name="del_contact", fax="573-092", nickname="2"))
            gen.contact.create(Contact(first_name="del_contact", fax="573-092", nickname="3"))
    with allure.step('When I click on "Select all" and then delete contacts with accept deletion'):
        gen.contact.del_by_select_all()
    with allure.step('Then the new contact list is empty'):
        assert 0 == len(db.get_contact_list())
        new_contact_list = db.get_contact_list()
        assert [] == new_contact_list
        if check_ui:
            assert sorted(new_contact_list, key=Contact.id_or_max) == sorted(gen.contact.get_contact_list(),
                                                                             key=Contact.id_or_max)


def test_del_all_contacts_click(gen, db, check_ui):
    with allure.step('Given a non-empty contact list'):
        if len(db.get_contact_list()) == 0:
            gen.contact.create(Contact(first_name="del_contact", fax="573-092", nickname="1"))
            gen.contact.create(Contact(first_name="del_contact", fax="573-092", nickname="2"))
            gen.contact.create(Contact(first_name="del_contact", fax="573-092", nickname="3"))
    with allure.step('When I choose each contact and then delete contacts with accept deletion'):
        gen.contact.del_all_by_click()
    with allure.step('Then the new contact list is empty'):
        assert 0 == len(db.get_contact_list())
        new_contact_list = db.get_contact_list()
        assert [] == new_contact_list
        if check_ui:
            assert sorted(new_contact_list, key=Contact.id_or_max) == sorted(gen.contact.get_contact_list(),
                                                                             key=Contact.id_or_max)


def test_del_unselected_contact(gen, db, check_ui):
    with allure.step('Given a non-empty contact list'):
        if len(db.get_contact_list()) == 0:
            gen.contact.create(Contact(first_name="del_contact", fax="573-092", nickname="1"))
            gen.contact.create(Contact(first_name="del_contact2", fax="573-092", nickname="2"))
        old_contact_list = db.get_contact_list()
    with allure.step('When I not select contact and then click by delete button'):
        gen.contact.del_unselected()
    with allure.step('Then the new contact list is equal to the old list without changes'):
        assert len(old_contact_list) == len(db.get_contact_list())
        new_contact_list = db.get_contact_list()
        assert sorted(new_contact_list, key=Contact.id_or_max) == sorted(new_contact_list, key=Contact.id_or_max)
        if check_ui:
            assert sorted(new_contact_list, key=Contact.id_or_max) == sorted(gen.contact.get_contact_list(),
                                                                             key=Contact.id_or_max)


def test_del_all_contacts_from_group(gen, orm, check_ui):
    with allure.step('Given a random group with contacts'):
        group = random.choice(orm.get_group_list())
        if len(orm.get_contact_in_group(group=group)) == 0:
            gen.contact.create(Contact(first_name="del_contact", fax="573-092", nickname="1", group_name=group.id))
            gen.contact.create(Contact(first_name="del_contact", fax="573-092", nickname="2", group_name=group.id))
            gen.contact.create(Contact(first_name="del_contact", fax="573-092", nickname="3", group_name=group.id))
    with allure.step('When I delete all contacts from the group "%s"' % group.name):
        gen.contact.del_all_from_group(group_id=group.id)
    with allure.step('Then the new contact list is empty'):
        assert 0 == len(orm.get_contact_in_group(group=group))
        new_contact_list = orm.get_contact_in_group(group=group)
        assert [] == new_contact_list
        if check_ui:
            assert sorted(new_contact_list, key=Contact.id_or_max) == sorted(
                gen.contact.get_contact_list(group_id=group.id), key=Contact.id_or_max)


def test_del_first_contact_from_group(gen, orm, check_ui):
    with allure.step('Given a random group with contacts'):
        group = random.choice(orm.get_group_list())
        if len(orm.get_contact_in_group(group=group)) == 0:
            gen.contact.create(Contact(first_name="del_contact", fax="573-092", nickname="1", group_name=group.id))
            gen.contact.create(Contact(first_name="del_contact", fax="573-092", nickname="2", group_name=group.id))
            gen.contact.create(Contact(first_name="del_contact", fax="573-092", nickname="3", group_name=group.id))
    with allure.step('Given contact list from the group "%s"' % group.name):
        old_contact_list = orm.get_contact_in_group(group=group, sorted=True)
    with allure.step('When I delete first contact from the group "%s"' % group.name):
        gen.contact.del_first_from_group(group_name=group.id)
    with allure.step('Then the new contact list is equal to the old list without the deleted contact'):
        assert len(old_contact_list) - 1 == len(orm.get_contact_in_group(group=group))
        new_contact_list = orm.get_contact_in_group(group=group)
        old_contact_list[0:1] = []
        assert sorted(new_contact_list, key=Contact.id_or_max) == sorted(new_contact_list, key=Contact.id_or_max)
        if check_ui:
            assert sorted(new_contact_list, key=Contact.id_or_max) == sorted(
                gen.contact.get_contact_list(group_id=group.id), key=Contact.id_or_max)


def test_del_some_contact_from_group(gen, orm, check_ui):
    with allure.step('Given a random group with contacts'):
        group = random.choice(orm.get_group_list())
        if len(orm.get_contact_in_group(group=group)) == 0:
            gen.contact.create(Contact(first_name="del_contact", fax="573-092", nickname="1", group_name=group.id))
            gen.contact.create(Contact(first_name="del_contact", fax="573-092", nickname="1", group_name=group.id))
            gen.contact.create(Contact(first_name="del_contact", fax="573-092", nickname="1", group_name=group.id))
    with allure.step('Given contact list from the group "%s"' % group.name):
        old_contact_list = orm.get_contact_in_group(group=group)
    with allure.step('Given a random contact from the list'):
        contact = random.choice(old_contact_list)
    with allure.step('When I delete contact from the group "%s"' % group.name):
        gen.contact.del_from_group_by_id(contact_id=contact.id, group_id=group.id)
    with allure.step('Then the new contact list is equal to the old list without the deleted contact'):
        assert len(old_contact_list) - 1 == len(orm.get_contact_in_group(group=group))
        new_contact_list = orm.get_contact_in_group(group=group)
        old_contact_list.remove(contact)
        assert sorted(new_contact_list, key=Contact.id_or_max) == sorted(new_contact_list, key=Contact.id_or_max)
        if check_ui:
            assert sorted(new_contact_list, key=Contact.id_or_max) == sorted(
                gen.contact.get_contact_list(group_id=group.id), key=Contact.id_or_max)


def test_del_first_contact_using_edit(gen, db, check_ui):
    with allure.step('Given a non-empty contact list'):
        if len(db.get_contact_list()) == 0:
            gen.contact.create(Contact(first_name="del_contact", fax="573-092", nickname="1"))
        old_contact_list = db.get_contact_list(sorted=True)
    with allure.step('When I delete first contact from the list using edit and accept deletion'):
        gen.contact.del_first_using_edit()
    with allure.step('Then the new contact list is equal to the old list without the deleted contact'):
        assert len(old_contact_list) - 1 == len(db.get_contact_list())
        new_contact_list = db.get_contact_list()
        old_contact_list[0:1] = []
        assert sorted(new_contact_list, key=Contact.id_or_max) == sorted(new_contact_list, key=Contact.id_or_max)
        if check_ui:
            assert sorted(new_contact_list, key=Contact.id_or_max) == sorted(gen.contact.get_contact_list(),
                                                                             key=Contact.id_or_max)


def test_del_some_contact_using_edit(gen, db, check_ui):
    with allure.step('Given a non-empty contact list'):
        if len(db.get_contact_list()) == 0:
            gen.contact.create(Contact(first_name="del_contact", fax="573-092", nickname="1"))
            gen.contact.create(Contact(first_name="del_contact", fax="573-092", nickname="1"))
            gen.contact.create(Contact(first_name="del_contact", fax="573-092", nickname="1"))
        old_contact_list = db.get_contact_list()
    with allure.step('Given a random contact from the list'):
        cid = int(random.choice(old_contact_list).id)
    with allure.step('When I delete contact from the list using edit and accept deletion'):
        gen.contact.del_using_edit_by_id(cid)
    with allure.step('Then the new contact list is equal to the old list without the deleted contact'):
        assert len(old_contact_list) - 1 == len(db.get_contact_list())
        new_contact_list = db.get_contact_list()
        old_contact_list[cid:cid+1] = []
        assert sorted(new_contact_list, key=Contact.id_or_max) == sorted(new_contact_list, key=Contact.id_or_max)
        if check_ui:
            assert sorted(new_contact_list, key=Contact.id_or_max) == sorted(gen.contact.get_contact_list(),
                                                                             key=Contact.id_or_max)


def test_del_all_search_result(gen, db, check_ui):
    with allure.step('Given a non-empty contact list and search string for it'):
        search = "lastname"
        if gen.contact.get_result_count(search=search) == 0:
            gen.contact.create(Contact(first_name="lastname", fax="573-092", nickname="1"))
            gen.contact.create(Contact(first_name="test", fax="573-092", nickname="lastname"))
            gen.contact.create(Contact(middle_name="lastname", fax="573-092", nickname="1"))
            gen.contact.create(Contact(last_name="lastname", fax="573-092", nickname="1"))
    # search_count = gen.contact.get_result_count(search=search)
    # old_contact_list = gen.contact.get_contact_list()
    with allure.step('When I delete all found contacts'):
        gen.contact.del_all_found(search)
    with allure.step('Then the new contact list is equal to the old list without deleted contacts'):
        assert 0 == gen.contact.get_result_count(search)
    # new_contact_list = gen.contact.get_contact_list()
