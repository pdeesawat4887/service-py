import re

regex = r"\/api\/(.*)\/([0-9]*$)"

test_str = "/api/service/4532ty"

# search = re.search(regex, test_str, re.M | re.I)
# search_obj = search.group(1)
# print search_obj
#
# result = re.findall(regex, test_str)
# if result.__len__() != 0:
#     print result[0]
# else:
#     print 'NONE'

# list_split = test_str.split('/')
# print list_split
#
# try:
#     condition = list_split[3]
# except:
#     condition = None
#
# print condition
#
# # hello = '/api/chart/probe_id/'
# # print hello.split('/')[2]
# # print hello
#
# lol = 'jk Lo'
# hek = """hello {} """.format(lol)
#
# grap = """Goodd Night {}""".format(lol)
#
# print ''.join([hek, grap])
#
# hello = ('abc', 123, 'NULL')
# new = str(hello)
#
# print new
#
# for k, v in dict.iteritems():
#     condition = "{}='{}'".format(k, v)
#     sql = ' and '.join([sql, condition])
#
# print sql
#
# def join_string(a, b):
#     return "{}='{}'".format(a, b)
#
# for k, v in dict.iteritems():
#     sql2 = ' and '.join([sql2, join_string(k, v)])
#
# print sql2

# print sql + ' and '.join(map(lambda item: "{}='{}'".format(item, dict[item]), dict))

# table = request.split('/')[2].split('?')[0]
# parameter = request.split('/')[2].split('?')[1]

# print table
# print parameter
#
# data = parameter.replace()
#
# print data

# sql = """SELECT {select} FROM {table} inner join destination on test_result.destination_id=destination.destination_id inner join service on service.service_id=destination.service_id""".format(
#             select='timestamp, destination.destination, rtt, download, upload, probe_id, test_result.destination_id',
#             table='test_result')

url = "192.168.254.31/api2/test_result/destination/destination_id/"

parameter = url.split('/')
table1 = parameter[2]
table2 = parameter[3]
table_condition = parameter[4]

sql12 = "SELECT {} FROM {} join {} on {}.{}={}.{}".format('*', table1, table2, table1, table_condition, table2, table_condition)

# print sql12
#
#
# print parameter
# print table1
# print table2
# print table_condition



import urlparse

# url = "192.168.254.31/api2/test_result/destination/destination_id?"
query = urlparse.urlsplit(url).query
params = dict(urlparse.parse_qsl(query))

# if len(params) is 0:
#         print "None"
# else:
#         print "Not None"
# map(lambda item: "{}.{}='{}'".format(self.table, item, condition[item]), condition)
#
# foo = "probe_id=123&ip_address=123.123.123.123"
#
# for i in  foo.split('&'):
#         print i

foo = "probe_id=123&ip_address=123.123.123.123"
select = "*"
table = 'probe'
sql = "SELECT {select} FROM {table}".format(select=select, table=table)



sql += " WHERE "+' and '.join(map(lambda item: "{}='{}'".format(item.split('=')[0], item.split('=')[1]), foo.split('&')))

# print sql

# foo ={'a': (1,2), 'b': 2, 'c': 3, 'e': 5}

# goo = foo.get('a', 0)
#
# print goo
# print type(goo)
#
# if type(foo) is str:
#     print foo

bar = "hello %s world %s foo %s %s"
test = [('apple', 'banana', 'cat', 'leo'), ('1', 2, 'three', 'FOUR')]

hello =  map(lambda item: bar % item, test)

print hello
print type(hello)

# for i in test:
#     print bar % i

import dns.resolver

if len(form) != 0:
    print 'hello'