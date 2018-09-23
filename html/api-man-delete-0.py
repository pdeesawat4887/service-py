#!/usr/bin/python

print "Content-Type: text/html\n"

import sys
import json
import json
import os
import main.database as mariadb
from datetime import date, datetime
import re


class DeleteMethod:

    def __init__(self, param_condition):
        self.create_delete_sql(param_condition)
        self.method_delete_action()

    def method_delete_action(self):
        db = mariadb.MySQLDatabase()
        for sql in self.sql:
            db.mycursor.execute(sql)
        db.connection.commit()

    def create_delete_sql(self, param_condition):
        self.sql = None


class DeleteService(DeleteMethod):

    def create_delete_sql(self, param_condition):
        parameter = param_condition.split('/')
        service_id = parameter[3]

        sql_running = "DELETE FROM running_serservice WHERE service_id={service_id}".format(service_id=service_id)
        sql_test_result = """DELETE FROM test_result 
        inner join destination on test_result.destination_id=destination.destination_id
        WHERE destination.service_id='{service_id}'""".format(service_id=service_id)
        sql_destination = "DELETE FROM destination WHERE service_id='{service_id}'".format(service_id=service_id)
        sql_service = "DELETE FROM service WHERE service_id='{service_id}'".format(service_id=service_id)

        self.sql = [sql_running, sql_test_result, sql_destination, sql_service]


sql = "DELETE FROM service WHERE service_id=13; DELETE FROM service WHERE service_id='14'"
# sql = "DELETE FROM service WHERE service_id='12'"
# operation = 'SELECT * From probe; SELECT * from pribe'
database = mariadb.MySQLDatabase()
database.mycursor.execute(sql, multi=True)
# print database.mycursor.fetchall()
database.connection.commit()
