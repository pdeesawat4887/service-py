#!/usr/bin/python

import json
import os
import main.database as mariadb
from datetime import date, datetime


class API:

    def __init__(self):
        self.identify_header()
        self.gen_sql()
        self.method_action()

    def identify_header(self):
        self.uri_split = os.environ['REQUEST_URI'].split('/')

    def gen_sql(self):
        self.sql = None

    def method_action(self):
        db = mariadb.MySQLDatabase()
        db.mycursor.execute(self.sql)
        row_headers = [x[0] for x in db.mycursor.description]
        rv = db.mycursor.fetchall()
        json_data = []
        for result in rv:
            json_data.append(dict(zip(row_headers, result)))
        print json.dumps(json_data, default=self.json_serial)

    def json_dump(self, obj):
        """JSON serializer for objects not serializable by default json code"""
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        print TypeError("Type %s not serializable" % type(obj))

    def json_serial(self, obj):
        """JSON serializer for objects not serializable by default json code"""
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        print TypeError("Type %s not serializable" % type(obj))


class MethodGet(API):

    def gen_sql(self):
        self.sql = "SELECT * FROM {}".format(self.uri_split[2])


if __name__ == '__main__':
    print "Access-Control-Allow-Origin: *"
    print "Content-Type: application/json\n"
    # print "Content-Type: text/html\n"

    method = os.environ['REQUEST_METHOD']
    uri_split = os.environ['REQUEST_URI'].split('/')

    method_dict = {
        'GET/3': MethodGet
    }

    word = method.upper() + '/' + str(len(uri_split))

    example = method_dict[word]()
