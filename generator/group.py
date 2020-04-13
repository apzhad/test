from model.group import Group
import random
import string
import os.path
import jsonpickle
import getopt
import sys


try:
    opts, args = getopt.getopt(sys.argv[1:], "cg:fg:", ["count of groups", "file for group data"])
except getopt.GetoptError as err:
    getopt.usage()
    sys.exit(2)


cg = 5
fg = "data/group.json"


for o, a in opts:
    if o == "-cg":
        cg = int(a)
    elif o == "-fg":
        fg = a


def random_string(prefix, max_length):
    symbols = string.ascii_letters + string.digits + ' '*10
    return prefix + "".join([random.choice(symbols) for i in range(random.randrange(max_length))])


test_data = [Group(name="", header="", footer="")] + [
    Group(name=random_string("name", 10), header=random_string("header_group", 20), footer=random_string("footer", 20))
    for i in range(cg)
]


data_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", fg)

with open(data_file, "w") as data:
    jsonpickle.set_encoder_options("json", indent=2)
    data.write(jsonpickle.encode(test_data))
