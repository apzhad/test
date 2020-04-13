# -*- coding: utf-8 -*-
from sys import maxsize
import re


class Group:

    def __init__(self, name=None, header=None, footer=None, id=None):
        self.name = name
        self.header = header
        self.footer = footer
        self.id = id

    def __repr__(self):
        return "%s:%s:%s:%s" % (self.id, self.name, self.header, self.footer)

    def __eq__(self, other):
        return (self.id is None or other.id is None or self.id == other.id) and self.normalize_name(self.name) == self.normalize_name(other.name)

    def id_or_max(self):
        if self.id:
            return int(self.id)
        else:
            return maxsize

    @staticmethod
    def normalize_name(name):
        if name is not None:
            if len(name) > 0:
                name = re.sub('\s+', ' ', name)
                name = name.strip()
        else:
            name = ""
        return name