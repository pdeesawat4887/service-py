#!/usr/bin/python

import json
import os
import main.database as mariadb
from datetime import date, datetime
import re


class Classify:

    def __init__(self):
        self.method = os.environ['REQUEST_METHOD']
        self.uri = os.environ['REQUEST_URI']
        print self.method
        print self.uri
        # self.classify_doing()

    def classify_doing(self):
        if self.method.lower() == 'get':
            operation = {
                'probes': GetMethodProbes,
                'probe': 1,
                'active': 2,
                'dest': 3,
                'user': 4,
                'warning': 5,
                'error': 6
            }
        else:
            operation = {

            }

        regex = r"\/api\/([a-z].*)"
        test_str = self.uri
        searchObj = re.search(regex, test_str, re.M | re.I)
        target = searchObj.group(1)
        print target
        example = operation[target]()


class GetMethod:

    def __init__(self):
        self.create_sql()
        self.method_action()

    def method_action(self):
        db = mariadb.MySQLDatabase()
        db.mycursor.execute(self.sql)
        row_headers = [x[0] for x in db.mycursor.description]
        rv = db.mycursor.fetchall()
        json_data = []
        for result in rv:
            json_data.append(dict(zip(row_headers, result)))
        print json.dumps(json_data, default=self.json_serial)

    def json_serial(self, obj):
        """JSON serializer for objects not serializable by default json code"""
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        print TypeError("Type %s not serializable" % type(obj))

    def create_sql(self):
        self.sql = None


class GetMethodProbes(GetMethod):

    def create_sql(self):
        self.sql = "SELECT * FROM probe"


# if __name__ == '__main__':
#     print "Access-Control-Allow-Origin: *"
#     # print "Content-Type: application/json\n"
#     print "Content-Type: text/html\n"
#     hello = Classify()

# regex = r"\/api\/([a-zA-Z0-9 ].*)\/([a-zA-Z0-9 ].*)\/([a-zA-Z0-9].*)\/([a-zA-Z0-9 ].*)"
#
# test_str = "/api/probes"
# test_str2 = "/api/probe/asd123dfse"
#
# searchObj = re.search(regex, test_str2, re.M | re.I)
# print searchObj.group(1)

path = '/api/probe/asdf123jkl'
path2 = '/api/active/1234586'
path3 = '/api/dest/789456'

list_url = [path, path2, path3]

path_s = path.split('/')
path2_s = path2.split('/')
path3_s = path3.split('/')

mod = path_s[2]
mod2 = path2_s[2]
mod3 = path3_s[2]

operation = {
    'probe': r"\/api\/([a-zA-Z0-9 ].*)\/([a-zA-Z0-9 ].*)",
    'active': r"\/api\/([a-zA-Z0-9 ].*)\/([a-zA-Z0-9 ].*)",
    'dest': r"\/api\/([a-zA-Z0-9 ].*)\/([a-zA-Z0-9 ].*)"
}

# regex = operation[mod]
for group in list_url:
    regex = operation[group.split('/')[2]]
    searchObj = re.search(regex, group, re.M | re.I)
    print searchObj.group(1)
    print searchObj.group(2)


class CreateSQL:

    def __init__(self):
        self.uri = os.environ['REQUEST_URI']
        self.method = os.environ['REQUEST_METHOD']

        self.dict_operation = {
            'probes': r"\/api\/([a-zA-Z ].*)",
            'probe': r"\/api\/([a-zA-Z0-9 ].*)\/([a-zA-Z0-9 ].*)",
            'active': r"\/api\/([a-zA-Z0-9 ].*)\/([a-zA-Z0-9 ].*)",
            'dest': r"\/api\/([a-zA-Z0-9 ].*)\/([a-zA-Z0-9 ].*)"
        }

        self.dict_table = {
            'probes': "probe",
            'probe': "probe",
            'active': "running_service",
            'dest': "destination"
        }

        self.dict_condition = {
            'probes': None,
            'probe': "probe_id",
            'active': "probe_id",
            'dest': "service_id"
        }

        self.classify_uri()
        self.create_sql()
        self.get_query()

    def classify_uri(self):
        regex = self.dict_operation[self.uri.split('/')[2]]
        self.searchObj = re.search(regex, self.uri, re.M | re.I)
        self.keyword = self.searchObj.group(1)

    def create_sql(self):

        if self.dict_condition[self.keyword] != None:
            self.parameter = self.searchObj.group(2)
            self.sql = "SELECT * FROM {} WHERE {}='{}'".format(self.dict_table[self.keyword],
                                                               self.dict_condition[self.keyword],
                                                               self.parameter)
        else:
            self.sql = "SELECT * FROM {}".format(self.dict_table)

    def get_query(self):
        db = mariadb.MySQLDatabase()
        db.mycursor.execute(self.sql)
        row_headers = [x[0] for x in db.mycursor.description]
        rv = db.mycursor.fetchall()
        json_data = []
        for result in rv:
            json_data.append(dict(zip(row_headers, result)))
        print json.dumps(json_data, default=self.json_serial)

    def json_serial(self, obj):
        """JSON serializer for objects not serializable by default json code"""
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        print TypeError("Type %s not serializable" % type(obj))


if __name__ == '__main__':
    print "Content-Type: application/json\n"
    # print "Content-Type: text/html\n"
    example = CreateSQL()
