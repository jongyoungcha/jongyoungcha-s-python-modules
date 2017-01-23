#-*- coding: utf-8 -*-

import sys
import os
from paramiko import client
import paramiko
import re


class ssh:
    client = None
    transport = None
    sftpclient = None

    lscmd="ls -R"

    def __init__(self, address, port, username, password):
        print("Connecting to server.")
        
        try:
            self.client = client.SSHClient()
            self.client.set_missing_host_key_policy(client.AutoAddPolicy())
            self.client.connect(address, username=username, password=password, look_for_keys=False)
        except Exception as e:
            print("connectting was failed ({0})".format(e))


        self.transport = paramiko.Transport((address, port))
        self.transport.connect(username = username, password=password)
        self.sftpclient = paramiko.SFTPClient.from_transport(self.transport)


    def send_command(self, command):
        if(self.client):
            stdin, stdout, stderr = self.client.exec_command(command)
            while not stdout.channel.exit_status_ready():
                # Print data when available
                if stdout.channel.recv_ready():
                    alldata = stdout.channel.recv(1024)
                    prevdata = b"1"
                    while prevdata:
                        prevdata = stdout.channel.recv(1024)
                        alldata += prevdata
                    print(str(alldata, 'utf8'))
        else:
            print("Connection not opened.")


    def upload_file(self, local_path, remote_path, relative_path):
        if(self.client):
            remote_full_path = "{0}/{1}".format(remote_path, relative_path)
            local_full_path = "{0}/{1}".format(local_path, relative_path)

            if(os.path.exists(local_full_path) and os.path.isfile(local_full_path)):
                self.sftpclient.put(local_full_path, relative_path)
            else:
                print("Local file was not existing.......")


    def get_local_directory_list(local_path):
        for root, dirs, files in os.walk(local_path):
            for file in files:
                print(file)


    def get_remote_directory_entries(self, remotepath, result):
        if(self.client):
            recved = ""
            alldata = None
            stdin, stdout, stderr = self.client.exec_command("find " + remotepath + " -type f -exec sha1sum {} \;")
            while not stdout.channel.exit_status_ready():
                # Print data when available
                if stdout.channel.recv_ready():
                    alldata = stdout.channel.recv(200000)
                    prevdata = b"1"
                    while prevdata:
                        prevdata = stdout.channel.recv(200000)
                        alldata += prevdata

                    recved += str(alldata, 'utf8')

            dic_entries = {}
            lst_entries = []
            for entry in recved.split('\n'):
                if entry is not '':
                    arr1=re.split(' .', entry)

                    print(arr1[0])
                    print(arr1[1])
                    print("===================================")

                    dic_entries.update({arr1[1]:arr1[0]})

            for key, value in dic_entries.items():
                print(key, value)

        else:
            print("Connection not opened.")

    def compare_directory_entries(self, remote_entries, local_entries):
        remote_en
        return None

        




if __name__=="__main__":
    result=0
    ssh=ssh('192.168.0.5', 22, 'jongyoungcha', 'a0319705971')
    ssh.send_command('ls')
    ssh.get_remote_directory_entries("/home/jongyoungcha/projects", result)

 
