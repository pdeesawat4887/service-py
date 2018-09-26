import main.database as db

database = db.MySQLDatabase()

# sql = "INSERT INTO service VALUES ('NULL', 'testDeleteService', 'NULL', 'HELOOWORLD')"
# database.mycursor.execute(sql)
#
#
#
# database.connection.commit()


# print database.mycursor.lastrowid

username = ['testAPI2_1', 'testAPI2_2']

# test_sql = "DELETE FROM user WHERE username = '%s' "
# test_sql = "DELETE FROM `project_monitor`.`user` WHERE  `username`='%s';"
#
# # list_del = map(lambda item: "DELETE FROM user WHERE username='{}'".format(item), username)
# try:
#     database.mycursor.executemany(test_sql, username)
#     database.connection.commit()
# except:
#     print 'ERROR'
    # print(database.mycursor.statement)
# database.connection.commit()

sql_list = map(lambda item: "DELETE FROM user WHERE username='{}'".format(item), username)
map(lambda sql: database.mycursor.execute(sql), sql_list)
database.connection.commit()