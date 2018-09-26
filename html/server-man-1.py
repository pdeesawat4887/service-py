#/usr/bin/python

import main.database as mariadb
import requests

class Warning:

    def __init__(self):
        self.db = mariadb.MySQLDatabase()
        self.prepare_statement()
        self.notify_line()

    def prepare_statement(self):
        self.sql = None
        self.msg_format = None

    def notify_line(self):
        url = 'https://notify-api.line.me/api/notify'
        token = 'pyL4xY6ys303vg0bVnvd0DRco7UyILVo5dOXZGjBWD8'
        headers = {'content-type': 'application/x-www-form-urlencoded', 'Authorization': 'Bearer ' + token}

        # print self.sql

        list_data = map(lambda item: self.msg_format % item, self.db.select(self.sql))

        for msg in list_data:
            request = requests.post(url, headers=headers, data={'message': msg})
            request.close()

class ProbeWarning(Warning):

    def prepare_statement(self):
        self.sql = """SELECT probe_name, ip_address, last_update FROM probe WHERE last_update < NOW() - INTERVAL 1 HOUR"""
        self.msg_format = "\nPROBE DOWN !!!\nProbe Name: %s\nIp Address: %s\nLast Update: %s\nPlease Check Your Probe"

    def update_probe_status(self):
        probes = self.db.select(self.sql)
        for probe in probes:
            update_sql = "UPDATE probe SET status='1' WHERE ip_address='{}'".format(probe[1])
            self.db.mycursor.execute(update_sql)
            self.db.connection.commit()

class GeneralServiceWarning(Warning):

    def prepare_statement(self):
        self.prepare_condition()
        self.sql = """SELECT timestamp, probe_name, ip_address, service_name, description, destination, destination_port, rtt, download, upload
                FROM test_result t1 JOIN destination t2 ON t1.destination_id=t2.destination_id
                JOIN service t3 ON t2.service_id=t3.service_id JOIN probe t4 ON t1.probe_id=t4.probe_id
                WHERE {condition} AND (timestamp > NOW() - INTERVAL {time} MINUTE) ORDER BY timestamp ASC""".format(time=10, condition=self.condition)
        self.msg_format = "\nWARNING !!!\nAt: %s\nProbe Name: %s\nIp Address: %s\nService Name: %s\nDescription: %s \nDestination: %s\nPort: %s\nRound-Trip-Time: %s ms.\nDownload: %s Mbps.\nUpload: %s Mbps.\nPlease Check Your Service."

    def prepare_condition(self):
        self.condition = """((t1.status!='0') or (download is NULL and upload is NULL and rtt > {rtt}))""".format(rtt=1000)

class VideoServiceWarning(GeneralServiceWarning):

    def prepare_condition(self):
        self.condition = """(download < {video_download} and upload is NULL)""".format(video_download=6)

class SpeedtestServiceWarning(GeneralServiceWarning):

    def prepare_condition(self):
        self.condition = """(download < {download} and upload < {upload})""".format(download=50, upload=10)

if __name__ == '__main__':
    warning_general = GeneralServiceWarning()
    warning_video = VideoServiceWarning()
    warning_speedtest = SpeedtestServiceWarning()
    warning_prone = ProbeWarning()
