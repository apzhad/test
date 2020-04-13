from model.contact import Contact
import string
import random
import jsonpickle
import os.path
import getopt
import sys


try:
    opts, args = getopt.getopt(sys.argv[1:], "cc:fc:", ["count of contacts", "file for contact data"])
except getopt.GetoptError as err:
    getopt.usage()
    sys.exit(2)


cc = 3
fc = "data/contact.json"


for o, a in opts:
    if o == "-cc":
        cc = int(a)
    elif o == "-fc":
        fc = a


def random_string(prefix, max_length):
    symbols = string.ascii_letters + string.digits + ' '*10
    return prefix + "".join([random.choice(symbols) for i in range(random.randrange(max_length))])


def random_string_with_eol(prefix, max_length):
    symbols = string.ascii_letters + string.digits + ' '*10 + '\n'*5
    return prefix + "".join([random.choice(symbols) for i in range(random.randrange(max_length))])


month = ("January", "February", "March", "April", "May", "June", "July",
         "August", "September", "October", "November", "December")


test_data = [Contact(first_name="", last_name="")] + [
    Contact(first_name=random_string("first_name", 20), middle_name=random_string("middle_name", 5),
            last_name=random_string("last_name", 10), nickname=random_string("nickname", 10),
            title=random_string("title", 10), company=random_string("company", 10),
            address=random_string_with_eol("address", 20), home_phone=random_string("homephone", 15),
            fax=random_string("fax", 15), primary_email=random_string("email", 10))
    for i in range(cc)
] + [
    Contact(first_name=random_string("first_name", 20), last_name=random_string("last_name", 10),
            title=random_string("title", 10), company=random_string("company", 10),
            mobile_phone=random_string("mobilephone", 15), work_phone=random_string("workphone", 15),
            secondary_email=random_string("email2", 10), third_email=random_string("email3", 10),
            homepage=random_string("homepage", 10))
    for m in range(cc)
] + [
    Contact(first_name=random_string("first_name", 20), last_name=random_string("last_name", 10),
            address=random_string_with_eol("address", 20), home_phone=random_string("homephone", 15),
            birth_day=str(random.randint(1, 31)), birth_month=random.choice(month), birth_year=random_string("", 10),
            anniversary_day=str(random.randint(1, 31)), anniversary_month=random.choice(month),
            anniversary_year=random_string("", 10), secondary_address=random_string_with_eol("sec_address", 20))
    for j in range(cc)
] + [
    Contact(first_name="", middle_name=random_string("middle_name", 5), last_name=random_string("last_name", 10),
            address=random_string_with_eol("address", 20), mobile_phone=random_string("mobilephone", 15),
            work_phone=random_string("workphone", 15), primary_email=random_string("email", 10),
            third_email=random_string("email3", 10), secondary_home_phone=random_string("sec_phone", 15),
            notes=random_string_with_eol("notes", 30), photo_path="i_tak.png")
    for k in range(cc)
]

data_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", fc)

with open(data_file, "w") as data:
    jsonpickle.set_encoder_options("json", indent=2)
    data.write(jsonpickle.encode(test_data))

