#!/usr/bin/python

import cgi
import os
import main.database as mysql
import json
from datetime import date, datetime
import decimal


# print "Content-Type: application/json\n"
# print "Content-Type: text/html\n"

# form = cgi.FieldStorage()
#
# regex = r"\/api-man\/(.+?)(?=\?)"
#
# start = "SELECT {select} FROM {table}"
#
# if len(form) == 0:
#     print 'empty'
# else:
#     print map(lambda item: "{condition}='{value}'".format(condition=item, value=form.getvalue(item)), form)

class GetMethod:

    def __init__(self, environ, form_data, select):
        self.database = mysql.MySQLDatabase()
        self.environ = environ
        self.form_data = form_data
        self.table = self.prepare_table()
        self.action(form_data, select)
        # print self.sql
        self.sql_action(self.sql)

    def action(self, form_data, select):
        self.prepare_statement(select)
        if len(form_data) != 0:
            self.prepare_condition(form_data)
        self.prepare_order()
        self.prepare_limit()

    def prepare_table(self):
        return self.environ['REDIRECT_URL'].split('/')[2]

    def prepare_statement(self, select):
        self.sql = "SELECT {select} FROM {table}".format(select=select, table=self.table)

    def prepare_condition(self, form):
        operation = None
        try:
            operation = self.environ['REDIRECT_URL'].split('/')[3]
        except:
            operation = "and"
        finally:
            self.sql += " WHERE " + ' {operation} '.format(operation=operation).join(
                map(lambda item: "{}='{}'".format(item, form.getvalue(item)), form))

    def prepare_order(self):
        pass

    def prepare_limit(self):
        pass

    def sql_action(self, sql_syntax):
        self.database.mycursor.execute(sql_syntax)
        row_headers = [x[0] for x in self.database.mycursor.description]
        rv = self.database.mycursor.fetchall()
        json_data = []
        for result in rv:
            json_data.append(dict(zip(row_headers, result)))
        print json.dumps(json_data, default=self.json_serial)

    def json_serial(self, obj):
        """JSON serializer for objects not serializable by default json code"""
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        print TypeError("Type %s not serializable" % type(obj))


class TestResult(GetMethod):

    def prepare_statement(self, select):
        self.sql = """SELECT {select} FROM test_result JOIN probe ON test_result.probe_id=probe.probe_id
        JOIN destination ON test_result.destination_id=destination.destination_id
        JOIN service ON service.service_id=destination.service_id""".format(select=select)

    def prepare_order(self):
        self.sql += " ORDER BY test_result.timestamp DESC"


class LimitTestResult(TestResult):

    def prepare_limit(self):
        self.sql += " Limit 10"


class RunningMethod(GetMethod):

    def prepare_statement(self, select):
        self.sql = """SELECT {select} FROM running_service 
        JOIN service ON running_service.service_id=service.service_id""".format(select=select)

    def prepare_order(self):
        self.sql += " ORDER BY service.service_id ASC"


class UserMethod(GetMethod):

    def action(self, form_data, select):
        try:
            username = form_data.getvalue('username')
        except:
            print '[]'
            exit()
        self.sql = "SELECT {select} FROM user WHERE username='{username}'".format(select=select, username=username)


class AvgTestResult(TestResult):

    def prepare_order(self):
        self.sql += " and timestamp > NOW() - INTERVAL 1 HOUR"


class CountTestResult:

    def __init__(self, environ, form_data, select):
        self.export_value(form_data)

    def prepare(self, service_id, probe_id):
        sql_all = """SELECT count(id) FROM test_result 
        JOIN destination ON test_result.destination_id=destination.destination_id
        WHERE service_id={service_id} and test_result.probe_id='{probe_id}'""".format(service_id=service_id,
                                                                                      probe_id=probe_id)

        sql_good = sql_all + " and test_result.status=0"

        count_all = self.execute_sql(sql_all)
        count_good = self.execute_sql(sql_good)
        return count_all, count_good

    def execute_sql(self, sql):
        db = mysql.MySQLDatabase()
        return db.select(sql)[0][0]

    def export_value(self, form_data):
        service_id = form_data.getvalue('service_id')
        probe_id = form_data.getvalue('probe_id')
        all, good = self.prepare(service_id, probe_id)
        data_dict = {'all': all, 'good': good}
        data_json = json.dumps(data_dict)
        print data_json


class PostMethod(GetMethod):

    def sql_action(self, list_data):
        self.database.insert(self.table, list_data)

    def prepare_statement(self, select):
        self.sql = ''


class DestinationMethod(PostMethod):

    def prepare_condition(self, form):
        self.sql = [(
            "NULL", form.getvalue('service_id'), form.getvalue('destination'), form.getvalue('destination_port', '0'),
            form.getvalue('description', None))]


class ServicePostMethod:

    def __init__(self, environ, form_data, select):
        self.database = mysql.MySQLDatabase()
        service_id = self.insert_service(form_data)
        self.insert_running_service(service_id)

    def insert_service(self, form_data):
        value = [('NULL', form_data.getvalue('service_name'), form_data.getvalue('file_name', None),
                  form_data.getvalue('command', None))]
        self.database.insert('service', value)
        return self.database.mycursor.lastrowid

    def insert_running_service(self, service_id):
        sql_all_probe = "SELECT probe_id FROM probe"
        list_all_probe = self.database.select(sql_all_probe)
        list_all_running = map(lambda item: (item[0], service_id, 1), list_all_probe)
        self.database.insert('running_service', list_all_running)


class DeleteDestinationMethod:

    def __init__(self, form):

        self.database = mysql.MySQLDatabase()
        self.prepare(form)

    def execute_sql(self, sql_syntax):
        self.database.delete(sql_syntax)
        # print self.sql

    def prepare(self, form):
        destination_id = form.getvalue('destination_id')
        where_condition = " WHERE destination_id='{destination_id}'".format(destination_id=destination_id)
        sql_test_result = "DELETE FROM test_result" + where_condition
        sql_destination = "DELETE FROM destination" + where_condition
        map(lambda item: self.execute_sql(item), [sql_test_result, sql_destination])


class DeleteServiceMethod(DeleteDestinationMethod):

    def prepare(self, form):
        service_id = form.getvalue('service_id')
        where_condition = " WHERE service_id='{service_id}'".format(service_id=service_id)
        sql_running = "DELETE FROM running_service" + where_condition
        sql_test_result = "DELETE test_result FROM test_result JOIN destination on test_result.destination_id=destination.destination_id" + where_condition
        sql_destination = "DELETE FROM destination" + where_condition
        sql_service = "DELETE FROM service" + where_condition
        map(lambda item: self.execute_sql(item), [sql_running, sql_test_result, sql_destination, sql_service])

class PatchMethod:

    def __init__(self, environ, form, table):
        self.prepare_statement(table)
        self.prepare_update(form)
        self.prepare_condition(environ)
        # print self.sql
        self.sql_action(self.sql)

    def prepare_statement(self, table):
        self.sql = "UPDATE {table} SET ".format(table=table)

    def prepare_update(self, form):
        self.sql += ', '.join(map(lambda item: "{}='{}'".format(item, form.getvalue(item)), form))

    def prepare_condition(self, environ):
        condition = environ['QUERY_STRING']
        self.sql += " WHERE " + ' and '.join(map(lambda item: "{}='{}'".format(item.split('=')[0], item.split('=')[1]), condition.split('&')))

    def sql_action(self, sql_syntax):
        self.database = mysql.MySQLDatabase()
        self.database.mycursor.execute(sql_syntax)
        self.database.connection.commit()


def check_information():
    for a in os.environ:
        print('Var: ', a, 'Value: ', os.getenv(a))
    print("all done")


if __name__ == '__main__':
    print "Content-Type: application/json\n"
    # print "Content-Type: text/html\n"
    form = cgi.FieldStorage()
    environ = os.environ
    dict_process = {
        'test_result': TestResult,
        'probe': GetMethod,
        'service': GetMethod,
        'running_service': RunningMethod,
        'destination': GetMethod,
        'user': UserMethod,
        'avg': AvgTestResult,
        'count': CountTestResult,
        'warning': LimitTestResult,
    }

    dict_select = {
        'test_result': '*',
        'probe': '*',
        'service': '*',
        'running_service': '*',
        'destination': '*',
        'user': 'password, role',
        'avg': 'round(avg(rtt), 2) as "rtt", round(avg(download), 2) as "download", round(avg(upload), 2) as "upload"',
        'count': None,
        'warning': 'probe_name, ip_address, service_name, destination, timestamp',
    }

    dict_post = {
        'service': ServicePostMethod,
        'destination': DestinationMethod,
    }

    dict_delete = {
        'service': DeleteServiceMethod,
        'destination': DeleteDestinationMethod
    }

    table = environ['REDIRECT_URL'].split('/')[2]
    request_method = environ['REQUEST_METHOD']
    # print request_method
    # print form

    if request_method.lower() == 'get':
        example = dict_process[table](environ, form, dict_select[table])
    elif request_method.lower() == 'post':
        example = dict_post[table](environ, form, None)
    elif request_method.lower() == 'delete':
        example = dict_delete[table](form)
    elif request_method.lower() == 'patch':
        example = PatchMethod(environ, form, None)