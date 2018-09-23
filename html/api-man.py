#!/usr/bin/python

import json
import cgi

import cgitb
import main.database as mariadb
from datetime import date, datetime

cgitb.enable()  # Optional; for debugging only


class API:

    def __init__(self):
        self.prepare_sql()
        self.databse_command()

    def prepare_sql(self):
        self.sql = None

    def get_variable(self, var_name):
        arguments = cgi.FieldStorage()
        return arguments[var_name].value

    def databse_command(self):
        database = mariadb.MySQLDatabase()
        database.mycursor.execute(self.sql)
        row_headers = [x[0] for x in database.mycursor.description]
        rv = database.mycursor.fetchall()
        json_data = []
        for result in rv:
            json_data.append(dict(zip(row_headers, result)))
        print json.dumps(json_data, default=self.json_serial)

    def json_serial(self, obj):
        """JSON serializer for objects not serializable by default json code"""
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        print TypeError("Type %s not serializable" % type(obj))


class GetTable(API):
    def prepare_sql(self):
        pass


class Chart(API):

    def prepare_sql(self):
        probe_id = self.get_variable('id')
        service_id = self.get_variable('service')
        dest_id = self.get_variable('dest_id')
        self.sql = """select timestamp, destination, upload, rtt, download 
        from test_result inner join destination on test_result.destination_id=destination.destination_id
        where status='0' and probe_id='{}' and service_id='{}' and destination.destination_id='{}'""".format(probe_id, service_id, dest_id)

    # def prepare_sql(self):
    #     self.sql = 'Chart chart ChArt'


def check_operation():
    print "Access-Control-Allow-Origin: *"
    print "Content-Type: application/json\n"
    # print "Content-Type: text/html\n"
    operation_dict = {
        'chart': Chart,
        'get': GetTable
    }

    arguments = cgi.FieldStorage()
    # print argument
    operation = arguments['operation'].value
    # print operation
    example = operation_dict[operation]()


if __name__ == '__main__':
    check_operation()
