#!/usr/bin/python

# import paramiko
# import os
# from stat import S_ISDIR


# class Prepare:

#     def __init__(self, remote_dir, local_dir):
#         self.hostname = "192.168.254.31"
#         self.username = "root"
#         self.password = "p@ssword"
#         self.remote_dir = remote_dir
#         self.local_dir = local_dir

#     def download_dir(self):
#         ssh = paramiko.SSHClient()
#         ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#         ssh.connect(hostname=self.hostname, username=self.username, password=self.password)
#         sftp = ssh.open_sftp()
#         os.path.exists(self.local_dir) or os.makedirs(self.local_dir)
#         dir_items = sftp.listdir_attr(self.remote_dir)
#         for item in dir_items:
#             # assuming the local system is Windows and the remote system is Linux
#             # os.path.join won't help here, so construct remote_path manually
#             remote_path = self.remote_dir + '/' + item.filename
#             local_path = os.path.join(self.local_dir, item.filename)
#             if S_ISDIR(item.st_mode):
#                 self.download_dir()
#             else:
#                 sftp.get(remote_path, local_path)

#     def chmod_file(self):
#         for root, dirs, files in os.walk(self.local_dir):
#             for d in dirs:
#                 os.chmod(os.path.join(root, d), 0705)
#             for f in files:
#                 os.chmod(os.path.join(root, f), 0705)


# if __name__ == '__main__':
#     LOCAL_DIR = "/root/get_upload"
#     REMOTE_DIR = "/root/upload"
#     prepare_probe = Prepare(REMOTE_DIR, LOCAL_DIR)
#     prepare_probe.download_dir()
#     # prepare_probe.chmod_file()

import paramiko
from stat import S_ISDIR
import os

def chmod_file(local_path):
    for root, dirs, files in os.walk(local_path):
        for d in dirs:
            os.chmod(os.path.join(root, d), 0705)
            os.chmod(os.path.join(root, d), 0705)
        for f in files:
            os.chmod(os.path.join(root, f), 0705)
            os.chmod(os.path.join(root, f), 0705)

def download_dir(remote_dir, local_dir):
    import os
    hostname = '192.168.254.31'
    username = 'root'
    password = 'p@ssword'

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
            download_dir(remote_path, local_path)
        else:
            sftp.get(remote_path, local_path)

download_dir('/root/monitor/', '/home/pi/get_upload/')
chmod_file('/home/pi/get_upload/')