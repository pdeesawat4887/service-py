#!/usr/bin/python

import socket
import re
import uuid
import database
import service
import paramiko
from stat import S_ISDIR
import base64
import os
import random
import string


class Probe:

    def __init__(self, path):
        LOCAL_DIR = '/root/release3/'
        REMOTE_DIR = '/root/release3_service/'
        self.path = path
        self.mac_address = self.get_mac_address()
        self.db = database.MySQLDatabase()
        self.ip = self.get_ip()
        self.id = self.get_probe_id()
        self.set_probe()
        # self.download_dir(REMOTE_DIR, LOCAL_DIR)
        # self.chmod_file(LOCAL_DIR)
        self.worker()

    def set_probe(self):
        query_sql = "SELECT * FROM probe WHERE probe_id='{}'".format(self.id)
        result = self.db.select(query_sql)
        if result.__len__() == 1:
            print "UPDATE"
            sql = "UPDATE probe SET ip_address='{}', mac_address='{}', status='{}', last_update=NOW() WHERE probe_id='{}'".format(
                self.ip, self.mac_address, 0, self.id)
            self.db.mycursor.execute(sql)
            self.db.connection.commit()
        else:
            print "INSERT NEW"
            sql = "INSERT INTO probe VALUES ('{}', NULL, '{}', '{}', '{}', NOW())".format(
                self.id, self.ip, self.mac_address, 0)
            self.db.mycursor.execute(sql)
            self.db.connection.commit()

            sql_service = self.db.select("SELECT service_id FROM service")
            result_running = map(lambda item: (self.id, item[0], 0), sql_service)
            self.db.insert('running_service', result_running)

    def get_mac_address(self):
        ''' Get MAC Address '''
        mac = ''.join(re.findall('..', '%012x' % uuid.getnode()))
        mac_address = ':'.join(mac[i:i + 2] for i in range(0, 12, 2))
        return mac_address

    def get_ip(self):
        ''' Get probe ip from source ip contain in socket that connect to 10.255.255.255 '''
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('10.255.255.255', 1))
            ip = s.getsockname()[0]
        except:
            ip = '127.0.0.1'
        finally:
            s.close()
        return ip

    def get_probe_id(self):
        ''' Create EUI64 from Mac Address for probe_id to collect in database '''
        # mac = mac.replace(':', '')
        # eui64 = mac[0:6] + 'fffe' + mac[6:]
        # eui64 = hex(int(eui64[0:2], 16) ^ 2)[2:].zfill(2) + eui64[2:]
        # return eui64
        FILE_PATH = "conf/configuration"
        if os.stat(FILE_PATH).st_size == 0:
            id = ''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(16))
            open(FILE_PATH, "wb").write(id)
        else:
            id = open(FILE_PATH, "r").readline()
        return id

    def get_active_service(self):
        query_sql = """select service.service_id, service.file_name, service.command 
        from service inner join running_service on service.service_id=running_service.service_id 
        where running_service.running_status=0 and probe_id='{}'""".format(self.id)
        result = self.db.select(query_sql)
        return result

    def download_dir(self, remote_dir, local_dir):
        hostname = '192.168.254.31'
        username = 'root'
        password = base64.b64decode('cEBzc3dvcmQ=')
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, username=username, password=password)
        sftp = ssh.open_sftp()
        os.path.exists(local_dir) or os.makedirs(local_dir)
        dir_items = sftp.listdir_attr(remote_dir)
        for item in dir_items:
            # assuming the local system is Windows and the remote system is Linux
            # os.path.join won't help here, so construct remote_path manually
            remote_path = remote_dir + '/' + item.filename
            local_path = os.path.join(local_dir, item.filename)
            if S_ISDIR(item.st_mode):
                self.download_dir(remote_path, local_path)
            else:
                sftp.get(remote_path, local_path)

    def chmod_file(self, local_path):
        for root, dirs, files in os.walk(local_path):
            for d in dirs:
                os.chmod(os.path.join(root, d), 0705)
            for f in files:
                os.chmod(os.path.join(root, f), 0705)

    def worker(self):
        service_active = self.get_active_service()
        # print service_active

        for service_instance in service_active:
            service_id = service_instance[0]
            service_file = service_instance[1]
            service_command = service_instance[2]

            if service_file is None:
                service_obj = service.Service(service_id, self.id, service_command)
            else:
                os.system('python {}/{} {} {} {}'.format(self.path, service_file, service_id, self.id, service_command))
