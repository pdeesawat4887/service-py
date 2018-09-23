#!/usr/bin/python

import json
import os
import main.database as mariadb
from datetime import date, datetime
import re


class CreateSQL:

    def __init__(self):
        self.uri = os.environ['REQUEST_URI']
        self.method = os.environ['REQUEST_METHOD']

        self.dict_operation = {
            'probes': r"\/api\/([a-zA-Z ].*)",
            'probe': r"\/api\/([a-zA-Z0-9 ].*)\/([a-zA-Z0-9 ].*)",
            'active': r"\/api\/([a-zA-Z0-9 ].*)\/([a-zA-Z0-9 ].*)",
            'dest': r"\/api\/([a-zA-Z0-9 ].*)\/([0-9]*$)",
            'user': r"\/api\/([a-zA-Z0-9 ].*)\/([a-zA-Z0-9 ].*)",
            'status': r"\/api\/([a-zA-Z0-9 ].*)\/([0-9 ]*$)",
            'result': r"\/api\/([a-zA-Z0-9 ].*)\/([a-zA-Z0-9 ].*)",
            'chart': r"\/api\/([a-zA-Z].*)\/([A-Za-z0-9].*)\/([0-9]*)\/([0-9]*)",
            'services': r"\/api\/([a-zA-Z ].*)",
            'running': r"\/api\/([a-zA-Z ].*)",
        }

        self.dict_table = {
            'probes': "probe",
            'probe': "probe",
            'active': "running_service",
            'dest': "destination",
            'user': "user",
            'status': "test_result",
            'result': "test_result",
            'chart': None,
            'services': "service",
            'running': "running_service"
        }

        self.dict_condition = {
            'probes': None,
            'probe': "probe_id",
            'active': None,
            'dest': "service_id",
            'user': "username",
            'status': "status",
            'result': "probe_id",
            'chart': None,
            'services': None,
            'running': None,
        }

        self.dict_select = {
            'probes': "*",
            'probe': "*",
            'active': "service_name",
            'dest': "*",
            'user': "password",
            'status': "*",
            'result': "*",
            'chart': "timestamp, destination, rtt, download, upload ",
            'services': "*",
            'running': "*",
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
            self.sql = "SELECT {} FROM {} WHERE {}='{}'".format(self.dict_select[self.keyword],
                                                                self.dict_table[self.keyword],
                                                                self.dict_condition[self.keyword],
                                                                self.parameter)
        elif self.keyword.lower() == 'chart':
            param_probe_id = self.searchObj.group(2)
            param_service_id = self.searchObj.group(3)
            param_destination_id = self.searchObj.group(4)
            self.sql = """SELECT {} 
            FROM test_result inner join destination on test_result.destination_id=destination.destination_id
            WHERE status='0' and probe_id='{}' and service_id='{}' and destination.destination_id='{}'""".format(
                self.dict_select[self.keyword.lower()], param_probe_id, param_service_id, param_destination_id)
        elif self.keyword.lower() == 'active':
            param_probe_id = self.searchObj.group(2)
            self.sql = """SELECT {} FROM running_service
            inner join service on running_service.service_id=service.service_id
            where running_status='0' and probe_id='{}'""".format(self.dict_select[self.keyword.lower()], param_probe_id)
        else:
            self.sql = "SELECT {} FROM {}".format(self.dict_select[self.keyword], self.dict_table[self.keyword])

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
    print "Access-Control-Allow-Origin: *"
    print "Content-Type: application/json\n"
    # print "Content-Type: text/html\n"
    example = CreateSQL()
