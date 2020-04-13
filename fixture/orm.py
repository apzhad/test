from pony.orm import *
from datetime import datetime
from model.group import Group
from model.contact import Contact
# from pymysql.converters import  decoders


class ORMFixture:

    db = Database()

    class ORMGroup(db.Entity):
        _table_ = 'group_list'
        id = PrimaryKey(int, column='group_id')
        name = Optional(str, column='group_name')
        header = Optional(str, column='group_header')
        footer = Optional(str, column='group_footer')
        contacts = Set(lambda: ORMFixture.ORMContact, table="address_in_groups", column="id", reverse="groups",
                       lazy=True)

    class ORMContact(db.Entity):
        _table_ = 'addressbook'
        id = PrimaryKey(int, column='id')
        firstname = Optional(str, column='firstname')
        lastname = Optional(str, column='lastname')
        deprecated = Optional(datetime, column='deprecated')
        home_phone = Optional(str, column='home')
        mobile_phone = Optional(str, column='mobile')
        work_phone = Optional(str, column='work')
        secondary_home_phone = Optional(str, column='phone2')
        primary_email = Optional(str, column='email')
        secondary_email = Optional(str, column='email2')
        third_email = Optional(str, column='email3')
        address = Optional(str, column='address')
        groups = Set(lambda: ORMFixture.ORMGroup, table="address_in_groups", column="group_id", reverse="contacts",
                     lazy=True)

    def __init__(self, host, name, user, password):
        self.db.bind('mysql', host=host, database=name, user=user, password=password)
        self.db.generate_mapping()
        sql_debug(True)

    def convert_gr_to_model(self, groups):
        def convert(group):
            return Group(id=str(group.id), name=group.name, header=group.header, footer=group.footer)
        return list(map(convert, groups))

    def convert_cont_to_model(self, contacts):
        def convert(contact):
            return Contact(id=str(contact.id), first_name=contact.firstname, last_name=contact.lastname,
                           address=contact.address, home_phone=contact.home_phone, mobile_phone=contact.mobile_phone,
                           work_phone=contact.work_phone, secondary_home_phone=contact.secondary_home_phone,
                           primary_email=contact.primary_email, secondary_email=contact.secondary_email,
                           third_email=contact.third_email)
        return list(map(convert, contacts))

    @db_session
    def get_group_list(self):
        return self.convert_gr_to_model(select(gr for gr in ORMFixture.ORMGroup))

    @db_session
    def get_contact_list(self):
        return self.convert_cont_to_model(select(c for c in ORMFixture.ORMContact if c.deprecated is None))

    @db_session
    def get_contact_in_group(self, group, sorted=False):
        orm_group = list(select(gr for gr in ORMFixture.ORMGroup if gr.id == group.id))[0]
        if not sorted:
            return self.convert_cont_to_model(
                select(c for c in ORMFixture.ORMContact if c.deprecated is None and orm_group in c.groups))
        else:
            return self.convert_cont_to_model(
                select(c for c in ORMFixture.ORMContact if c.deprecated is None and orm_group in c.groups).order_by(
                    ORMFixture.ORMContact.lastname, ORMFixture.ORMContact.firstname))

    @db_session
    def get_contact_not_in_group(self, group):
        orm_group = list(select(gr for gr in ORMFixture.ORMGroup if gr.id == group.id))[0]
        return self.convert_cont_to_model(
            select(c for c in ORMFixture.ORMContact if c.deprecated is None and orm_group not in c.groups))

