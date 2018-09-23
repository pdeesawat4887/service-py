#!/usr/bin/python

import mysql.connector


class MySQLDatabase:

    def __init__(self):
        self.host = '192.168.254.31'
        self.user = 'monitor'
        self.password = 'p@ssword'
        # self.database = 'project'
        self.database = 'project_monitor'

        # self.host = '192.168.1.8'
        # self.user = 'centos'
        # self.password = 'root'
        # self.database = 'project_monitor'

        # self.host = '192.168.1.8'
        # self.user = 'centos'
        # self.password = 'root'
        # self.database = 'project_monitor'

        self.create_connection()

    def create_connection(self):
        try:
            self.connection = mysql.connector.connect(
                user=self.user, password=self.password, host=self.host, database=self.database)
            self.mycursor = self.connection.cursor()
        except Exception as error:
            print "Error database:", error

    def select(self, sql_query):
        self.mycursor.execute(sql_query)
        return self.mycursor.fetchall()

    def insert(self, table, list_data):
        query = "INSERT INTO %s " % table
        query += "VALUES (" + ",".join(["%s"] * len(list_data[0])) + ")"

        self.mycursor.executemany(query, list_data)
        self.connection.commit()

    def close_connection(self):
        self.mycursor.close()
        self.connection.disconnect()

# from datetime import date, datetime
# def json_serial(obj):
#     """JSON serializer for objects not serializable by default json code"""
#
#     if isinstance(obj, (datetime, date)):
#         return obj.isoformat()
#     raise TypeError ("Type %s not serializable" % type(obj))
#
# if __name__ == '__main__':
#     import json
#     json_data = []
#     database = MySQLDatabase()
#     sql = 'SELECT * FROM probe'
#     result = database.select(sql)
#     row_headers = [x[0] for x in database.mycursor.description]
#     for result in result:
#         json_data.append(dict(zip(row_headers, result)))
#     print json.dumps(json_data, default=json_serial)
