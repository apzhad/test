from model.contact import Contact
import random
import allure


def find_index(contacts, id):
    index = 0
    for c in contacts:
        if c.id == id:
            break
        index += 1
    return index


def test_edit_first_contact(gen, check_ui, db):
    with allure.step('Given a non-empty contact list'):
        if len(db.get_contact_list()) == 0:
            gen.contact.create(Contact(first_name="modify"))
        old_contact_list = db.get_contact_list(sorted=True)
    with allure.step('Given a data for modify contact'):
        cont = Contact(first_name="new_name", middle_name="new_middle_name", last_name="lastname",
                       nickname="nick", title="title234", company="company2", address="address12",
                       home_phone="home", mobile_phone="mobile", work_phone="work",
                       fax="fax123", primary_email="email_pri", secondary_email="",
                       third_email="", homepage="home", birth_day="4",
                       birth_month="July", birth_year="1978", anniversary_day="9",
                       anniversary_month="May", anniversary_year="2008",
                       secondary_address="sec_addr", secondary_home_phone="",
                       notes="s jv s\njsbej", photo_path="3.png")
    cont.id = old_contact_list[0].id
    with allure.step('When I modify the first contact from the list'):
        gen.contact.edit_first(cont)
    with allure.step('Then the new contact list is equal to the old list with modified contact'):
        assert len(old_contact_list) == len(db.get_contact_list())
        new_contact_list = db.get_contact_list()
        old_contact_list[0] = cont
        assert sorted(old_contact_list, key=Contact.id_or_max) == sorted(new_contact_list, key=Contact.id_or_max)
        if check_ui:
            assert sorted(new_contact_list, key=Contact.id_or_max) == sorted(gen.contact.get_contact_list(),
                                                                             key=Contact.id_or_max)


def test_edit_some_contact(gen, check_ui, db):
    with allure.step('Given a non-empty contact list'):
        if len(db.get_contact_list()) == 0:
            gen.contact.create(Contact(first_name="modify"))
        old_contact_list = db.get_contact_list()
    with allure.step('Given a random contact from the list'):
        cid = random.choice(old_contact_list).id
    with allure.step('Given a data for modify contact'):
        cont = Contact(first_name="new_name", middle_name="new_middle_name", last_name="lastname",
                       nickname="nick", title="title234", company="company2", address="address12",
                       home_phone="home", mobile_phone="mobile", work_phone="work",
                       fax="fax123", primary_email="email_pri", secondary_email="",
                       third_email="", homepage="home", birth_day="4",
                       birth_month="July", birth_year="1978", anniversary_day="9",
                       anniversary_month="May", anniversary_year="2008",
                       secondary_address="sec_addr", secondary_home_phone="",
                       notes="s jv s\njsbej", photo_path="3.png", id=cid)
    with allure.step('When I modify the contact from the list'):
        gen.contact.edit_by_id(cid, cont)
    index = find_index(old_contact_list, cid)
    with allure.step('Then the new contact list is equal to the old list with modified contact'):
        assert len(old_contact_list) == len(db.get_contact_list())
        new_contact_list = db.get_contact_list()
        old_contact_list[index] = cont
        assert sorted(old_contact_list, key=Contact.id_or_max) == sorted(new_contact_list, key=Contact.id_or_max)
        if check_ui:
            assert sorted(new_contact_list, key=Contact.id_or_max) == sorted(gen.contact.get_contact_list(),
                                                                             key=Contact.id_or_max)


def test_edit_first_contact_without_change(gen, check_ui, db):
    with allure.step('Given a non-empty contact list'):
        if len(db.get_contact_list()) == 0:
            gen.contact.create(Contact(first_name="modify", last_name="status"))
        old_contact_list = db.get_contact_list(sorted=True)
    with allure.step('When I modify the first contact from the list without changes'):
        gen.contact.edit_first_wo_change()
    with allure.step('Then the new contact list is equal to the old list'):
        assert len(old_contact_list) == len(db.get_contact_list())
        new_contact_list = db.get_contact_list()
        assert sorted(old_contact_list, key=Contact.id_or_max) == sorted(new_contact_list, key=Contact.id_or_max)
        if check_ui:
            assert sorted(new_contact_list, key=Contact.id_or_max) == sorted(gen.contact.get_contact_list(),
                                                                             key=Contact.id_or_max)


def test_edit_some_contact_without_change(gen, check_ui, db):
    with allure.step('Given a non-empty contact list'):
        if len(db.get_contact_list()) == 0:
            gen.contact.create(Contact(first_name="modify", last_name="status"))
        old_contact_list = db.get_contact_list()
    with allure.step('Given a random contact from the list'):
        cid = random.choice(old_contact_list).id
    with allure.step('When I modify the contact from the list without changes'):
        gen.contact.edit_wo_change_by_id(cid)
    with allure.step('Then the new contact list is equal to the old list'):
        assert len(old_contact_list) == len(db.get_contact_list())
        new_contact_list = db.get_contact_list()
        assert sorted(old_contact_list, key=Contact.id_or_max) == sorted(new_contact_list, key=Contact.id_or_max)
        if check_ui:
            assert sorted(new_contact_list, key=Contact.id_or_max) == sorted(gen.contact.get_contact_list(),
                                                                             key=Contact.id_or_max)


def test_edit_first_contact_in_group(gen, check_ui, orm):
    with allure.step('Given a random group with contacts'):
        group = orm.get_group_list()
        group = random.choice(group)
        if len(orm.get_contact_in_group(group=group)) == 0:
            gen.contact.create(Contact(first_name="modify", last_name="status", group_name=group.id))
    with allure.step('Given contact list from the group "%s"' % group.name):
        old_contact_list = orm.get_contact_in_group(group=group, sorted=True)
    with allure.step('Given a data for modify contact'):
        cont = Contact(first_name="first", last_name="last", address="gjh")
    with allure.step('When I modify the first contact in the group "%s"' % group.name):
        gen.contact.edit_first_in_group(group_name=group.id, contact=cont)
    with allure.step('Then the new contact list is equal to the old list with modified contact'):
        assert len(old_contact_list) == len(orm.get_contact_in_group(group=group))
        new_contact_list = orm.get_contact_in_group(group=group)
        cont.id = old_contact_list[0].id
        old_contact_list[0] = cont
        assert sorted(old_contact_list, key=Contact.id_or_max) == sorted(new_contact_list, key=Contact.id_or_max)
        if check_ui:
            assert sorted(new_contact_list, key=Contact.id_or_max) == sorted(gen.contact.get_contact_list(
                group_id=group.id), key=Contact.id_or_max)


def test_edit_some_contact_in_group(gen, check_ui, orm):
    with allure.step('Given a random group with contacts'):
        group = random.choice(orm.get_group_list())
        if len(orm.get_contact_in_group(group=group)) == 0:
            gen.contact.create(Contact(first_name="modify", last_name="status", group_name=group.id))
    with allure.step('Given contact list from the group "%s"' % group.name):
        old_contact_list = orm.get_contact_in_group(group=group)
    with allure.step('Given a random contact from the list'):
        cid = random.choice(old_contact_list).id
    with allure.step('Given a data for modify contact'):
        cont = Contact(first_name="first", last_name="last", address="gjh", id=cid)
    with allure.step('When I modify the contact in the group "%s"' % group.name):
        gen.contact.edit_in_group_by_id(id=cid, group_id=group.id, contact=cont)
    with allure.step('Then the new contact list is equal to the old list with modified contact'):
        assert len(old_contact_list) == len(orm.get_contact_in_group(group=group))
        index = find_index(old_contact_list, cid)
        new_contact_list = orm.get_contact_in_group(group=group)
        old_contact_list[index] = cont
        assert sorted(old_contact_list, key=Contact.id_or_max) == sorted(new_contact_list, key=Contact.id_or_max)
        if check_ui:
            assert sorted(new_contact_list, key=Contact.id_or_max) == sorted(gen.contact.get_contact_list(
                group_id=group.id), key=Contact.id_or_max)


def test_edit_first_contact_from_details(gen, check_ui, db):
    with allure.step('Given a non-empty contact list'):
        if len(db.get_contact_list()) == 0:
            gen.contact.create(Contact(first_name="modify", last_name="status"))
        old_contact_list = db.get_contact_list(sorted=True)
    with allure.step('Given a data for modify contact'):
        cont = Contact(first_name="name", middle_name="middle", last_name="last",
                       nickname="", title="", company="cmp", address="none",
                       home_phone="32445", mobile_phone="", work_phone="763728",
                       homepage="", birth_day="-", birth_month="-", birth_year="",
                       anniversary_day="-", anniversary_month="-", anniversary_year="",
                       group_name="", secondary_address="", secondary_home_phone="",
                       notes="", del_foto=True)
    cont.id = old_contact_list[0].id
    with allure.step('When I open details and modify the first contact from the list'):
        gen.contact.edit_first_from_details(cont)
    with allure.step('Then the new contact list is equal to the old list with modified contact'):
        assert len(old_contact_list) == len(db.get_contact_list())
        new_contact_list = db.get_contact_list()
        old_contact_list[0] = cont
        assert sorted(old_contact_list, key=Contact.id_or_max) == sorted(new_contact_list, key=Contact.id_or_max)
        if check_ui:
            assert sorted(new_contact_list, key=Contact.id_or_max) == sorted(gen.contact.get_contact_list(),
                                                                             key=Contact.id_or_max)


def test_edit_some_contact_from_details(gen, check_ui, db):
    with allure.step('Given a non-empty contact list'):
        if len(db.get_contact_list()) == 0:
            gen.contact.create(Contact(first_name="modify", last_name="status"))
        old_contact_list = db.get_contact_list()
    with allure.step('Given a random contact from the list'):
        cid = random.choice(old_contact_list).id
    index = find_index(old_contact_list, cid)
    with allure.step('Given a data for modify contact'):
        cont = Contact(first_name="name", middle_name="middle", last_name="last",
                       nickname="", title="", company="cmp", address="none",
                       home_phone="32445", mobile_phone="", work_phone="763728",
                       homepage="", birth_day="-", birth_month="-", birth_year="",
                       anniversary_day="-", anniversary_month="-", anniversary_year="",
                       group_name="", secondary_address="", secondary_home_phone="",
                       notes="", del_foto=True, id=cid)
    with allure.step('When I open details and modify the contact from the list'):
        gen.contact.edit_from_details_by_id(cid, cont)
    with allure.step('Then the new contact list is equal to the old list with modified contact'):
        assert len(old_contact_list) == len(db.get_contact_list())
        new_contact_list = db.get_contact_list()
        old_contact_list[index] = cont
        assert sorted(old_contact_list, key=Contact.id_or_max) == sorted(new_contact_list, key=Contact.id_or_max)
        if check_ui:
            assert sorted(new_contact_list, key=Contact.id_or_max) == sorted(gen.contact.get_contact_list(),
                                                                             key=Contact.id_or_max)


def test_add_all_contacts_to_group(gen, check_ui, orm):
    with allure.step('Given a random group'):
        group = random.choice(orm.get_group_list())
    with allure.step('Given a non-empty contact list'):
        if len(orm.get_contact_list()) == 0:
            gen.contact.create(Contact(first_name="modify", last_name="change_group", group_name=group.id))
            gen.contact.create(Contact(first_name="modify_1", last_name="change_group_1", group_name="[none]"))
            gen.contact.create(Contact(first_name="modify_2", last_name="change_group_2"))
        old_contact_list = orm.get_contact_list()
    with allure.step('When I add all contacts to the group "%s"' % group.name):
        gen.contact.add_all_to_group_using_id(group_id=group.id)
    with allure.step('Then the new contact list is equal to the old list'):
        assert len(old_contact_list) == len(orm.get_contact_list())
        new_contact_list = orm.get_contact_in_group(group=group)
        assert sorted(old_contact_list, key=Contact.id_or_max) == sorted(new_contact_list, key=Contact.id_or_max)
        if check_ui:
            assert sorted(new_contact_list, key=Contact.id_or_max) == sorted(
                gen.contact.get_contact_list(group_id=group.id), key=Contact.id_or_max)


def test_add_some_contact_to_group(gen, check_ui, orm):
    with allure.step('Given a random group'):
        group = random.choice(orm.get_group_list())
    with allure.step('Given a non-empty contact list'):
        if len(orm.get_contact_list()) == 0:
            gen.contact.create(Contact(first_name="modify", last_name="change_group", group_name=group.id))
            gen.contact.create(Contact(first_name="modify_1", last_name="change_group_1", group_name="[none]"))
            gen.contact.create(Contact(first_name="modify_2", last_name="change_group_2"))
        old_contact_list = orm.get_contact_in_group(group)
    with allure.step('Given a random contact from the list'):
        contact = random.choice(orm.get_contact_list())
    with allure.step('When I add contact to the group "%s"' % group.name):
        gen.contact.add_some_to_group_using_id(group_id=group.id, contact_id=contact.id)
    with allure.step('Then the contact is exist in the group'):
        if contact not in old_contact_list:
            assert len(old_contact_list) + 1 == len(orm.get_contact_in_group(group))
            old_contact_list.append(contact)
        else:
            assert len(old_contact_list) == len(orm.get_contact_in_group(group))
        new_contact_list = orm.get_contact_in_group(group=group)
        assert sorted(old_contact_list, key=Contact.id_or_max) == sorted(new_contact_list, key=Contact.id_or_max)
        if check_ui:
            assert sorted(new_contact_list, key=Contact.id_or_max) == sorted(
                gen.contact.get_contact_list(group_id=group.id), key=Contact.id_or_max)


def test_add_to_group_without_select_contact(gen, check_ui, orm):
    with allure.step('Given a random group'):
        group = random.choice(orm.get_group_list())
    with allure.step('Given a non-empty contact list'):
        if len(orm.get_contact_list()) == 0:
            gen.contact.create(Contact(first_name="modify", last_name="change_group"))
        old_contact_list = orm.get_contact_in_group(group)
    with allure.step('When I add to the group "%s" without choose contact' % group.name):
        gen.contact.add_to_group_unselected_using_id(group_id=group.id)
    with allure.step('Then the new contact list is equal to the old list'):
        assert len(old_contact_list) == len(orm.get_contact_in_group(group))
        new_contact_list = orm.get_contact_in_group(group)
        assert sorted(old_contact_list, key=Contact.id_or_max) == sorted(new_contact_list, key=Contact.id_or_max)
        if check_ui:
            assert sorted(new_contact_list, key=Contact.id_or_max) == sorted(
                gen.contact.get_contact_list(group_id=group.id), key=Contact.id_or_max)


def test_add_all_contacts_to_group_from_another_group(gen, check_ui, orm):
    with allure.step('Given a random group with contacts from which will be contacts added'):
        group_from = random.choice(orm.get_group_list())
    with allure.step('Given a random group to which will be contacts added'):
        group_to = random.choice(orm.get_group_list())
    with allure.step('Given a non-empty contact list in from group "%s"' % group_from.name):
        if len(orm.get_contact_in_group(group_from)) == 0:
            gen.contact.create(Contact(first_name="modify", last_name="change_group", group_name=group_from.id))
        from_list = orm.get_contact_in_group(group_from)
    with allure.step('Given a non-empty contact list in from group "%s"' % group_to.name):
        old_to_list = orm.get_contact_in_group(group_to)
    with allure.step('When I add all contacts from the group "%s" to the group "%s"' % (group_from.name, group_to.name)):
        gen.contact.add_to_group_from_another_using_id(id_from=group_from.id, id_to=group_to.id)
    with allure.step('Then contacts are exist in the "to" group'):
        assert len(from_list) + len(old_to_list) == len(orm.get_contact_in_group(group_to)) or len(
            from_list) == len(orm.get_contact_in_group(group_to))
        new_to_list = orm.get_contact_in_group(group_to)
        if sorted(old_to_list, key=Contact.id_or_max) != sorted(new_to_list, key=Contact.id_or_max):
            old_to_list = old_to_list + from_list
            assert sorted(old_to_list, key=Contact.id_or_max) == sorted(new_to_list, key=Contact.id_or_max)
        if check_ui:
            assert sorted(new_to_list, key=Contact.id_or_max) == sorted(
                gen.contact.get_contact_list(group_id=group_to.id), key=Contact.id_or_max)


def test_add_some_contact_to_group_from_another_group(gen, check_ui, orm):
    with allure.step('Given a random group with contacts from which will be contact added'):
        group_from = random.choice(orm.get_group_list())
    with allure.step('Given a random group to which will be contact added'):
        group_to = random.choice(orm.get_group_list())
    with allure.step('Given a non-empty contact list in from group "%s"' % group_from.name):
        if len(orm.get_contact_in_group(group_from)) == 0:
            gen.contact.create(Contact(first_name="modify", last_name="change_group", group_name=group_from.id))
        from_list = orm.get_contact_in_group(group_from)
    with allure.step('Given a random contact in the group from which it will be added'):
        contact = random.choice(from_list)
    with allure.step('Given a non-empty contact list in from group "%s"' % group_to.name):
        old_to_list = orm.get_contact_in_group(group_to)
    with allure.step('When I add contact from the group "%s" to the group "%s"' % (group_from.name, group_to.name)):
        gen.contact.add_some_contact_to_group_from_another(contact_id=contact.id, id_from=group_from.id,
                                                           id_to=group_to.id)
    with allure.step('Then contact is exist in the "to" group'):
        if contact in old_to_list:
            assert len(old_to_list) == len(orm.get_contact_in_group(group_to))
        else:
            assert len(old_to_list) + 1 == len(orm.get_contact_in_group(group_to))
        new_to_list = orm.get_contact_in_group(group_to)
        if sorted(old_to_list, key=Contact.id_or_max) != sorted(new_to_list, key=Contact.id_or_max):
            old_to_list.append(contact)
            assert sorted(old_to_list, key=Contact.id_or_max) == sorted(new_to_list, key=Contact.id_or_max)
        if check_ui:
            assert sorted(new_to_list, key=Contact.id_or_max) == sorted(
                gen.contact.get_contact_list(group_id=group_to.id), key=Contact.id_or_max)


def test_remove_all_contacts_from_group(gen, check_ui, orm):
    with allure.step('Given a random group with contacts'):
        group = random.choice(orm.get_group_list())
        if len(orm.get_contact_in_group(group)) == 0:
            gen.contact.create(Contact(first_name="modify", last_name="change_group", group_name=group.id))
            gen.contact.create(Contact(first_name="modify", last_name="change_group", group_name=group.id))
            gen.contact.create(Contact(first_name="modify", last_name="change_group", group_name=group.id))
    with allure.step('When I remove all contacts from the group'):
        gen.contact.remove_all_from_group(group_id=group.id)
    with allure.step('Then there are no contacts in the group'):
        assert 0 == len(orm.get_contact_in_group(group))
        cont_group_list = orm.get_contact_in_group(group)
        assert [] == cont_group_list
        if check_ui:
            assert sorted(cont_group_list, key=Contact.id_or_max) == sorted(
                gen.contact.get_contact_list(group_id=group.id), key=Contact.id_or_max)


def test_remove_some_contact_from_group(gen, check_ui, orm):
    with allure.step('Given a random group with contacts'):
        group = random.choice(orm.get_group_list())
        if len(orm.get_contact_in_group(group)) == 0:
            gen.contact.create(Contact(first_name="modify", last_name="change_group", group_name=group.id))
            gen.contact.create(Contact(first_name="modify", last_name="change_group", group_name=group.id))
            gen.contact.create(Contact(first_name="modify", last_name="change_group", group_name=group.id))
        old_contact_list = orm.get_contact_in_group(group)
    with allure.step('Given a random contact in the group "%s"' % group.name):
        contact = random.choice(orm.get_contact_in_group(group))
    with allure.step('When I remove contact from the group "%s"' % group.name):
        gen.contact.remove_some_from_group(group_id=group.id, contact_id=contact.id)
    with allure.step('Then contact is not exist in the group "%s"' % group.name):
        assert len(old_contact_list)-1 == len(orm.get_contact_in_group(group))
        new_contact_list = orm.get_contact_in_group(group)
        old_contact_list.remove(contact)
        assert sorted(old_contact_list, key=Contact.id_or_max) == sorted(new_contact_list, key=Contact.id_or_max)
        if check_ui:
            assert sorted(new_contact_list, key=Contact.id_or_max) == sorted(
                gen.contact.get_contact_list(group_id=group.id), key=Contact.id_or_max)


def test_edit_first_found_contact(gen, check_ui, db):
    with allure.step('Given a non-empty contact list and search string for it'):
        search = "modify"
        """
        query from database looks like 
        
        "SELECT `firstname` FROM `addressbook` 
        WHERE `firstname` LIKE '%name%' AND `lastname` LIKE '%name%' AND `deprecated` IS NULL "
        """
        if gen.contact.get_result_count(search) == 0:
            gen.contact.create(Contact(first_name=search, fax="573-092", nickname="1"))
        old_contact_list = gen.contact.get_contact_list(search=search)
    with allure.step('Given a data for modify contact'):
        cont = Contact(first_name="sbcghdhj", middle_name="j,lk", last_name="cgxh",
                       nickname="", title="dfg", company="lkg", address="",
                       home_phone="", work_phone="", fax="", homepage="", birth_day="22",
                       birth_month="April", birth_year="1234", anniversary_day="3",
                       anniversary_month="May", anniversary_year="77",
                       group_name="", secondary_address="dfg", secondary_home_phone="55",
                       notes="group")
    with allure.step('When I modify first found contact'):
        gen.contact.edit_first_found(search=search, contact=cont)
    cont.id = old_contact_list[0].id
    with allure.step('Then the new contact list is equal to the old list with modified contact'):
        assert len(old_contact_list) == gen.contact.get_contact_count()
        new_contact_list = gen.contact.get_contact_list(search=cont.first_name)
        old_contact_list[0] = cont
        assert sorted(old_contact_list, key=Contact.id_or_max) == sorted(new_contact_list, key=Contact.id_or_max)
