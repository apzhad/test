# -*- coding: utf-8 -*-
from sys import maxsize
import re


class Contact:

    def __init__(self, first_name=None, middle_name=None, last_name=None, nickname=None, title=None, company=None,
                 address=None, home_phone=None, mobile_phone=None, work_phone=None, fax=None, primary_email=None,
                 secondary_email=None, third_email=None, homepage=None, birth_day=None, birth_month=None,
                 birth_year=None, anniversary_day=None, anniversary_month=None, anniversary_year=None, group_name=None,
                 secondary_address=None, secondary_home_phone=None, notes=None, photo_path=None, del_foto=False,
                 id=None, all_phones=None, all_email=None):
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.nickname = nickname
        self.title = title
        self.company = company
        self.address = address
        self.home_phone = home_phone
        self.mobile_phone = mobile_phone
        self.work_phone = work_phone
        self.fax = fax
        self.primary_email = primary_email
        self.secondary_email = secondary_email
        self.third_email = third_email
        self.homepage = homepage
        self.birth_day = birth_day
        self.birth_month = birth_month
        self.birth_year = birth_year
        self.anniversary_day = anniversary_day
        self.anniversary_month = anniversary_month
        self.anniversary_year = anniversary_year
        self.group_name = group_name
        self.secondary_address = secondary_address
        self.secondary_home_phone = secondary_home_phone
        self.notes = notes
        self.photo_path = photo_path
        self.del_foto = del_foto
        self.id = id
        self.all_phones = all_phones
        self.all_email = all_email

    def __repr__(self):
        return "%s: %s %s" % (self.id, self.last_name, self.first_name)

    def __eq__(self, other):
        return ((self.id is None or other.id is None or self.id == other.id)
                and self.normalize_name(self.first_name) == self.normalize_name(other.first_name)
                and self.normalize_name(self.last_name) == self.normalize_name(other.last_name))

    def id_or_max(self):
        if self.id:
            return int(self.id)
        else:
            return maxsize

    @staticmethod
    def normalize_name(parameter):
        if parameter is not None:
            if len(parameter) > 0:
                parameter = re.sub('\s+', ' ', parameter)
                parameter = parameter.strip()
        else:
            parameter = ""
        return parameter
