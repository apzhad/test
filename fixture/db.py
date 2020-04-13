import pymysql.cursors
from model.group import Group
from model.contact import Contact


class DbFixture:

    def __init__(self, host, name, user, password):
        self.host = host
        self.name = name
        self.user = user
        self.password = password
        self.connection = pymysql.connect(host=host, database=name, user=user, password=password, autocommit=True)

    def get_group_list(self, sorted=False):
        cursor = self.connection.cursor()
        group_list = []
        try:
            if not sorted:
                cursor.execute("select group_id, group_name, group_header, group_footer from group_list")
            else:
                cursor.execute("select group_id, group_name, group_header, group_footer from group_list "
                               "ORDER BY group_name")
            for row in cursor:
                (id, name, header, footer) = row
                group_list.append(Group(id=str(id), name=name, header=header, footer=footer))
        finally:
            cursor.close()
        return group_list

    def get_contact_list(self, sorted=False):
        cursor = self.connection.cursor()
        contact_list = []
        try:
            if not sorted:
                cursor.execute("select id, firstname, lastname from addressbook "
                               "where deprecated = '0000-00-00 00:00:00'")
            else:
                cursor.execute(
                    "select id, firstname, lastname from addressbook where deprecated = '0000-00-00 00:00:00' "
                    "ORDER BY firstname, lastname")
            for row in cursor:
                (id, firstname, lastname) = row
                contact_list.append(Contact(id=str(id), first_name=firstname, last_name=lastname))
        finally:
            cursor.close()
        return contact_list

    def finish(self):
        self.connection.close()
