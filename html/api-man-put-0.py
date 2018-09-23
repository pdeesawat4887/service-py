#!/usr/bin/python


print "Content-Type: text/html\n"

import json
import main.database as mariadb


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
