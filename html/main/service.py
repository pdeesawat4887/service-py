#!/usr/bin/python

import database
import bitmath
import socket
import time


class Service:

    def __init__(self, service_id, probe_id, command):
        self.service_id = service_id
        self.probe_id = probe_id
        self.command = command
        self.db = database.MySQLDatabase()
        print self.collect_data()

    def query_destination(self):
        query_sql = "SELECT destination_id, destination, destination_port FROM destination WHERE service_id='{}'".format(
            self.service_id)
        return self.db.select(query_sql)

    def collect_data(self):

        info_test_result = []
        destinations = self.query_destination()
        time_insert = time.strftime('%Y-%m-%d %H:%M:%S')

        if len(destinations) == 0:
            return "No destination in service: {}".format(self.service_id)
        else:
            for dest in destinations:
                temp_id = dest[0]
                temp_dest = dest[1]
                temp_port = dest[2]

                info_test = ('NULL', self.probe_id, temp_id, time_insert,)
                info_result = self.get_status(temp_dest, temp_port)

                info_test_result.append(info_test + info_result)

            self.db.insert('test_result', info_test_result)
            return "Successfully insert service: {}".format(self.service_id)

    def get_status(self, destination, port):
        timeout = 1
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        start = time.time()
        s.settimeout(timeout)
        try:
            s.connect((destination, port))
            if self.command != None:
                s.send(self.command)
                resp = s.recv(1024)
            # print resp
            return 0, (time.time() - start) * 1000, None, None
        except socket.timeout:
            return 1, timeout, None, None
        except Exception as error:
            return 2, timeout, None, None
        finally:
            s.close()

    def round_to_n_decimal(self, value, digit):
        return round(float(value), digit)

    def convert_bps_to_mbps(self, num_of_bytes):
        bit = bitmath.Bit(num_of_bytes)
        return bit.to_Mib().value

    def convert_bps_to_mbps2(self, num_of_bytes):
        bit = bitmath.Byte(num_of_bytes)
        return bit.to_MiB().value
