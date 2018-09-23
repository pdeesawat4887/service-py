#!/usr/bin/python

import json
import os
import sys
import main.database as mariadb
from datetime import date, datetime
import cgi

class Method:

    def __init__(self, select, table, table_condition, condition):
        self.sql = None
        self.table = table
        self.action(select, table, table_condition, condition)

    def action(self, select, table, table_condition, condition):
        self.prepare_statement(select, table)

        if condition != None and condition != '':
            self.prepare_condition(condition)

        self.method_action()

    def method_action(self):
        db = mariadb.MySQLDatabase()
        db.mycursor.execute(self.sql)
        db.connection.commit()

    def prepare_statement(self, select, table):
        self.sql = "SELECT {select} FROM {table}".format(select=select, table=table)

    def prepare_condition(self, condition):
        if type(condition) is str:
            self.sql += " WHERE " + ' and '.join(
                map(lambda item: "{}.{}='{}'".format(self.table, item.split('=')[0], item.split('=')[1]),
                    condition.split('&')))
        else:
            self.sql += " WHERE " + ' and '.join(
                map(lambda item: "{}.{}='{}'".format(self.table, item, condition.getvalue(item)), condition))


class GetMethod(Method):

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


class TestResultMethod(GetMethod):

    def prepare_statement(self, select, table):
        self.sql = """SELECT {} FROM test_result 
        JOIN destination ON test_result.destination_id=destination.destination_id
        JOIN service ON service.service_id=destination.service_id""".format(select)


class RunningMethod(GetMethod):

    def prepare_statement(self, select, table):
        self.sql = """SELECT {} FROM running_service
        JOIN service ON running_service.service_id=service.service_id
        JOIN probe ON running_service.probe_id=probe.probe_id""".format(select)


class UserMethod(GetMethod):

    def action(self, select, table, table_condition, condition):
        if len(condition) == 0:
            print '[]'
            exit()
        else:
            self.prepare_statement(select, table)
            self.prepare_condition(condition)
            self.method_action()


class PostMethod(Method):

    def action(self, select, table, table_condition, condition):

        self.tuple_insert = self.prepare_insert(table, condition)
        self.sql = "INSERT INTO {table} VALUES (".format(table=table) + ",".join(["%s"] * len(self.tuple_insert)) + ")"
        self.method_action()

    def method_action(self):
        db = mariadb.MySQLDatabase()
        db.mycursor.execute(self.sql, self.tuple_insert)
        db.connection.commit()

    def prepare_insert(self, table, condition):
        if table == 'destination':
            return ('NULL', condition.getvalue('service_id'), condition.getvalue('destination'),
                    condition.getvalue('destination_port', '0'))
        elif table == 'running_service':
            return (
            condition.getvalue('probe_id'), condition.getvalue('service_id'), condition.getvalue('running_status'))
        elif table == 'service':
            return (condition.getvalue('service_id', 'NULL'), condition.getvalue('service_name'),
                    condition.getvalue('file_name', 'NULL'), condition.getvalue('command', 'NULL'))


class DeleteMethod(Method):

    def prepare_statement(self, select, table):
        self.sql = "DELETE FROM {table}".format(table=table)


class PatchMethod(Method):

    def action(self, select, table, table_condition, condition):
        self.sql = "UPDATE {table} SET ".format(table=table)
        self.prepare_update(condition)
        if len(table_condition) != 0:
            self.prepare_condition(table_condition)
        self.method_action()

    def prepare_update(self, condition):
        self.sql += ', '.join(map(lambda item: "{}='{}'".format(item, condition.getvalue(item)), condition))


if __name__ == '__main__':
    print "Access-Control-Allow-Origin: *"
    print "Content-Type: application/json\n"

    dict_method = {
        'destination': GetMethod,
        'probe': GetMethod,
        'running_service': RunningMethod,
        'service': GetMethod,
        'test_result': TestResultMethod,
        'user': UserMethod,
    }

    dict_select = {
        'destination': '*',
        'probe': '*',
        'running_service': '*',
        'service': '*',
        'test_result': '*',
        'user': 'password, role',
    }

    url = os.environ['REDIRECT_URL']
    method = os.environ['REQUEST_METHOD']

    parameter = url.split('/')
    table1 = parameter[2]
    table_condition = None
    form = cgi.FieldStorage()

    if method == 'GET':
        try:
            condition = json.loads(sys.stdin.read())
        except ValueError:
            condition = os.environ['QUERY_STRING']
        example = dict_method[table1](dict_select[table1], table1, table_condition, condition)
    elif method == 'POST':
        example = PostMethod(dict_select[table1], table1, table_condition, form)
    elif method == 'DELETE':
        example = DeleteMethod(dict_select[table1], table1, table_condition, form)
    elif method == "PATCH":
        example = PatchMethod(dict_select[table1], table1, os.environ['QUERY_STRING'], form)
