#!/usr/bin/python

import json
import cgi
import cgitb
import main.database as mariadb
from datetime import date, datetime
cgitb.enable()  # Optional; for debugging only


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    print TypeError("Type %s not serializable" % type(obj))


def hello():
    # print "Content-Type: application/json\n"
    print "Content-Type: text/html\n"
    arguments = cgi.FieldStorage()
    # table = arguments['table'].value
    print arguments
    operation = arguments['operation'].value

    operation_dict = {
        'chart': chart,
        'get': get
    }
    # print len(arguments)

    # sql = 'SELECT * from {}'.format(table)
    # database = mariadb.MySQLDatabase()
    # database.mycursor.execute(sql)
    # row_headers = [x[0] for x in database.mycursor.description]
    # rv = database.mycursor.fetchall()
    # json_data = []
    # for result in rv:
    #     json_data.append(dict(zip(row_headers, result)))
    # print json.dumps(json_data, default=json_serial)

def chart():
    pass

def get():
    pass

def prototype(sql):
    database = mariadb.MySQLDatabase()
    database.mycursor.execute(sql)
    row_headers = [x[0] for x in database.mycursor.description]
    rv = database.mycursor.fetchall()
    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))
    print json.dumps(json_data, default=json_serial)


def check_url():
    print "Content-Type: application/json\n"
    arguments = cgi.FieldStorage()
    probe_id = arguments['id'].value
    service_id = arguments['service'].value
    time = arguments['time'].value
    sql = """select * from test_result inner join destination on test_result.destination_id=destination.destination_id 
    where probe_id='{}' and service_id='{}'""".format(probe_id, service_id)
    prototype(sql)


hello()
# check_url()

# class API:

#   url = 'www.google.com'

# helo = API()
# helo.hello_api()
