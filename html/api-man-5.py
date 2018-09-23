#!/usr/bin/python

import json
import os
import sys
import main.database as mariadb
from datetime import date, datetime
import re


class GetMethod:

    def __init__(self, param_condition):
        self.create_sql(param_condition)
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

    def create_sql(self, param_condition_uri):
        self.sql = None


class GetProbe(GetMethod):

    def create_sql(self, param_condition_uri):
        parameter = param_condition_uri.split('/')
        self.sql = """SELECT {select} FROM {table}""".format(select='*', table='probe')
        try:
            probe_id = parameter[3]
            condition_probe_id = """WHERE probe_id='{probe_id}'""".format(probe_id=probe_id)
            self.sql = ' '.join([self.sql, condition_probe_id])
        except:
            probe_id = None


class GetService(GetMethod):

    def create_sql(self, param_condition_uri):
        parameter = param_condition_uri.split('/')
        self.sql = """SELECT {select} FROM {table}""".format(select='*', table='service')
        try:
            service_id = parameter[3]
            condition_service_id = """WHERE service_id='{service_id}'""".format(service_id=service_id)
            self.sql = ' '.join([self.sql, condition_service_id])
        except:
            service_id = None


class GetActiveService(GetMethod):

    def create_sql(self, param_condition_uri):
        param_condition = param_condition_uri.split('/')[3]
        self.sql = """SELECT {select} FROM running_service
            inner join service on running_service.service_id=service.service_id
            where running_status='0' and probe_id='{param}'""".format(select='service.service_id, service_name',
                                                                      param=param_condition)


class GetDestination(GetMethod):

    def create_sql(self, param_condition_uri):
        parameter = param_condition_uri.split('/')
        self.sql = """SELECT {select} FROM {table}""".format(select='*', table='destination')
        try:
            service_id = parameter[3]
            condition_service_id = """WHERE service_id='{service_id}'""".format(service_id=service_id)
            self.sql = ' '.join([self.sql, condition_service_id])
        except:
            service_id = None


class GetUser(GetMethod):

    def create_sql(self, param_condition_uri):
        param_condition = param_condition_uri.split('/')[3]
        self.sql = """SELECT {select} FROM {table} WHERE {condition}='{param}'""".format(select='password',
                                                                                         table='user',
                                                                                         condition='username',
                                                                                         param=param_condition)


class GetStatus(GetMethod):

    def create_sql(self, param_condition_uri):
        parameter = param_condition_uri.split('/')
        self.sql = """SELECT {select} FROM {table} inner join destination on test_result.destination_id=destination.destination_id inner join service on service.service_id=destination.service_id""".format(
            select='timestamp, destination.destination, rtt, download, upload, probe_id, test_result.destination_id',
            table='test_result')
        try:
            status = parameter[3]
            condition_status = """WHERE status='{status}'""".format(status=status)
            self.sql = ' '.join([self.sql, condition_status])
        except:
            status = None
        try:
            probe_id = parameter[4]
            condition_probe_id = """and probe_id='{probe_id}'""".format(probe_id=probe_id)
            self.sql = ' '.join([self.sql, condition_probe_id])
        except:
            probe_id = None
        try:
            service_id = parameter[5]
            condition_service_id = """and destination.service_id='{service_id}'""".format(service_id=service_id)
            self.sql = ' '.join([self.sql, condition_service_id])
        except:
            service_id = None
        try:
            destination_id = parameter[6]
            condition_destination_id = """and test_result.destination_id='{destination_id}'""".format(
                destination_id=destination_id)
            self.sql = ' '.join([self.sql, condition_destination_id])
        except:
            destination_id = None


class GetChart(GetMethod):

    def create_sql(self, param_condition_uri):
        parameter = param_condition_uri.split('/')
        self.sql = """SELECT {select} FROM test_result inner join destination on test_result.destination_id=destination.destination_id""".format(
            select='timestamp, destination, rtt, download, upload')
        try:
            probe_id = parameter[3]
            condition_probe_id = """WHERE status='{status}' and probe_id='{probe_id}'""".format(status='0',
                                                                                                probe_id=probe_id)
            self.sql = ' '.join([self.sql, condition_probe_id])
        except:
            probe_id = None
        try:
            service_id = parameter[4]
            condition_service_id = """and service_id='{service_id}'""".format(service_id=service_id)
            self.sql = ' '.join([self.sql, condition_service_id])
        except:
            service_id = None
        try:
            destination_id = parameter[5]
            condition_destination_id = """and test_result.destination_id='{destination_id}'""".format(
                destination_id=destination_id)
            self.sql = ' '.join([self.sql, condition_destination_id])
        except:
            destination = None


class GetRunningService(GetMethod):

    def create_sql(self, param_condition_uri):
        self.sql = """SELECT {select} FROM running_service
        inner join service on running_service.service_id=service.service_id
        inner join probe on running_service.probe_id=probe.probe_id""".format(
            select='probe.probe_id, probe.probe_name, service.service_id, service.service_name, running_service.running_status')


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
        self.sql = "INSERT INTO {table} VALUES (".format(table=self.table) + ",".join(["%s"] * len(self.pattern)) + ")"
        # query += " VALUES (" + ",".join(["%s"] * len(list_data[0])) + ")"
        # print self.sql
        db.mycursor.execute(self.sql, self.pattern)
        db.connection.commit()


class PostDestination(PostMethod):

    def create_pattern(self, data_dict):
        self.pattern = ('NULL', data_dict['service_id'], data_dict['destination'], data_dict['destination_port'])


class PostService(PostMethod):

    def create_pattern(self, data_dict):
        self.pattern = ('NULL', data_dict['service_name'], data_dict['file_name'], data_dict['command'])


class PostRunningService(PostMethod):

    def create_pattern(self, data_dict):
        self.pattern = (data_dict['probe_id'], data_dict['service_id'], data_dict['running_status'])


class PostUser(PostMethod):

    def create_pattern(self, data_dict):
        self.pattern = (data_dict['username'], data_dict['password'], data_dict['salt'], data_dict['role'])


class PutMethod:

    def __init__(self, table, data):
        self.table = table
        data_dict = json.loads(data)
        self.update_sql(data_dict)
        self.method_update()

    def update_sql(self, data_dict):
        self.sql = None

    def method_update(self):
        db = mariadb.MySQLDatabase()
        db.mycursor.execute(self.sql)
        db.connection.commit()


class PutService(PutMethod):

    def update_sql(self, data_dict):
        self.sql = "UPDATE service SET"
        try:
            service_name = data_dict['service_name']
            set_service_name = """service_name='{service_name}'""".format(service_name=service_name)
            self.sql = ' '.join([self.sql, set_service_name])
        except:
            service_name = None
        try:
            file_name = data_dict['file_name']
            set_file_name = """file_name='{file_name}'""".format(file_name=file_name)
            self.sql = ' '.join([self.sql, set_file_name])
        except:
            file_name = None
        try:
            command = data_dict['command']
            set_command = """command='{command}'""".format(command=command)
            self.sql = ' '.join([self.sql, set_command])
        except:
            command = None
        finally:
            service_id = data_dict['service_id']
            condition = "WHERE service_id={service_id}".format(service_id=service_id)
            self.sql = ' '.join([self.sql, condition])


class PutDestination(PutMethod):

    def update_sql(self, data_dict):
        self.sql = "UPDATE destination SET"
        try:
            destination = data_dict['destination']
            set_destination = """destination='{destination}'""".format(destination=destination)
            self.sql = ' '.join([self.sql, set_destination])
        except:
            destination = None
        try:
            destination_port = data_dict['destination_port']
            set_destination_port = """destination_port='{destination_port}'""".format(destination_port=destination_port)
            self.sql = ' '.join([self.sql, set_destination_port])
        except:
            destination_port = None
        finally:
            destination_id = data_dict['destination_id']
            condition = "WHERE destination_id={destination_id}".format(destination_id=destination_id)
            self.sql = ' '.join([self.sql, condition])


class PutProbe(PutMethod):

    def update_sql(self, data_dict):
        self.sql = "UPDATE probe SET"
        try:
            probe_name = data_dict['probe_name']
            set_probe_name = """probe_name='{probe_name}'""".format(probe_name=probe_name)
            self.sql = ' '.join([self.sql, set_probe_name])
        except:
            probe_name = None
        finally:
            probe_id = data_dict['probe_id']
            condition = "WHERE probe_id={probe_id}".format(probe_id=probe_id)
            self.sql = ' '.join([self.sql, condition])


class PutRunningService(PutMethod):

    def update_sql(self, data_dict):
        self.sql = "UPDATE running_service SET"
        try:
            running_status = data_dict['running_status']
            set_running_status = """running_status='{running_status}'""".format(running_status=running_status)
            self.sql = ' '.join([self.sql, set_running_status])
        except:
            running_status = None
        finally:
            probe_id = data_dict['probe_id']
            service_id = data_dict['service_id']
            condition = "WHERE probe_id={probe_id} and service_id={service_id}".format(probe_id=probe_id,
                                                                                       service_id=service_id)
            self.sql = ' '.join([self.sql, condition])


if __name__ == '__main__':
    print "Access-Control-Allow-Origin: *"
    print "Content-Type: application/json\n"
    # print "Content-Type: text/html\n"
    uri = os.environ['REQUEST_URI']
    method = os.environ['REQUEST_METHOD']
    # target = uri.split('/')[2]

    print sys.stdin.read()
    print method
    print uri

    # if method == 'GET':
    #     dict_get = {
    #         'probe': GetProbe,
    #         'service': GetService,
    #         'active': GetActiveService,
    #         'destination': GetDestination,
    #         'user': GetUser,
    #         'status': GetStatus,
    #         'running': GetRunningService,
    #         'chart': GetChart,
    #     }
    #     example = dict_get[target](uri)
    # elif method == 'POST':
    #     dict_post = {
    #         'destination': PostDestination,
    #         'running': PostRunningService,
    #         'service': PostService,
    #         'user': PostUser
    #     }
    #     example = dict_post[target](target, sys.stdin.read())
    # elif method == 'PUT':
    #     dict_put = {
    #         'service': PutService,
    #         'destination': PutDestination,
    #         'probe': PutProbe,
    #         'running': PutRunningService,
    #     }
    #     example = dict_put[target](sys.stdin.read())
    # else:
    #     dict_get = {'test': None}

def get():
    import cgi
    print "Access-Control-Allow-Origin: *"
    # print "Content-Type: application/json\n"
    print "Content-Type: text/html\n"
    arguments = cgi.FieldStorage()
    probe_id = arguments.getvalue('probe_id')
    service_id = arguments.getvalue('service_id')
    destination_id = arguments.getvalue('destination_id')
    print probe_id, '<br>'
    print service_id, '<br>'
    print destination_id, '<br>'

get()