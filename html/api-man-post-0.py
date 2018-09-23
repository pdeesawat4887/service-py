#!/usr/bin/python

print "Content-Type: text/html\n"

import sys
import json
import json
import os
import main.database as mariadb
from datetime import date, datetime
import re

data = sys.stdin.read()
# print dict(data)
data_new = json.loads(data)
print type(data_new)
print data_new

class PostMethod:

    def __init__(self, table, data):
        self.table = table
        data_dict = json.loads(data)
        self.create_pattern(data_dict)
        self.method_insert()

    def create_pattern(self, data_dict):
        self.pattern = None

    def method_insert(self):
        db = mariadb.MySQLDatabase()
        self.sql = """INSERT INTO {table} VALUES {value}""".format(table=self.table, value=self.pattern)
        db.mycursor.execute(self.sql)
        db.connection.commit()

class PostDestination(PostMethod):

    def create_pattern(self, data_dict):
        self.pattern = str(('NULL', data_dict['service_id'], data_dict['destination'], data_dict['destination_port']))


class PostService(PostMethod):

    def create_pattern(self, data_dict):
        self.pattern = str(('NULL', data_dict['service_name'], data_dict['file_name'], data_dict['command']))

class PostRunningService(PostMethod):

    def create_pattern(self, data_dict):
        self.pattern = str((data_dict['probe_id'], data_dict['service_id'], data_dict['running_status']))

class PostUser(PostMethod):

    def create_pattern(self, data_dict):
        self.pattern = str((data_dict['username'], data_dict['password'], data_dict['salt'], data_dict['role']))

