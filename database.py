from fixture.orm import ORMFixture
from model.group import Group
from model.contact import Contact


db = ORMFixture(host="127.0.0.1", name="addressbook", user="root", password="")


try:
    group = Group(id="300")
    c = db.get_contact_list(search="name")
    for item in c:
        print(item)
    print(len(c))


finally:
    pass
