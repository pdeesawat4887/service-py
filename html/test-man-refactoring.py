import main.database as db
import time


database = db.MySQLDatabase()

sql_service = database.select("SELECT service_id FROM service")

result_running = []


for_time_start = time.time()
for service in sql_service:
    temp = ('probe_id', service[0], 0)
    result_running.append(temp)
for_time_end = time.time()
print for_time_start
print for_time_end

map_time_start = time.time()
result = map(lambda item: ('probe_id', item[0], 0), sql_service)
map_time_end = time.time()


print result_running, (for_time_end-for_time_start)

print result, (map_time_end-map_time_start)

# sql_service = self.db.select("SELECT service_id FROM service")
#             result_running = []
#             for serv in sql_service:
#                 temp = (self.id, serv[0], 0)
#                 result_running.append(temp)
#             self.db.insert('running_service', result_running)