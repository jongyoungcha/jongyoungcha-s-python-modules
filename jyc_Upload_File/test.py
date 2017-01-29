import sys
import paramiko
import os
import json

class sshuploader:
    transport = None
    sshclient = None
    sftpclient = None
    host = None
    id = None
    passwd = None
    localbasepath = None
    remotebasepath = None
    uploaded_file = None

    def __init__(self, config_file_path, uploaded_file):
        try:
            # Check file was existing
            if os.path.exists(config_file_path) is None:
                return None

            self.parse_config_file(config_file_path)
            uploaded_file = uploaded_file

            print("host:{0}".format(self.host))
            print("port:{0}".format(self.port))
            print("id:{0}".format(self.id))
            print("passwd:{0}".format(self.passwd))
            print("localbasepath:{0}".format(self.localbasepath))
            print("remotebasepath:{0}".format(self.remotebasepath))

            self.transport = paramiko.Transport((self.host, int(self.port)))
            self.transport.connect(username=self.id, password=self.passwd)

            self.sftpclient = paramiko.SFTPClient.from_transport(self.transport)

        except SSHException("ssh connection error") as e:
            print(e)

        except ssh_exception.AuthenticationException as e:
            print(e)



    def connect_ssh(self):
        self.sshclient = paramiko.SSHClient()
        self.sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.sshclient.connect(self.host, self.port, self.id, self.passwd)
        return None


    def disconnect_ssh(self):
        self.sshclient.close()
        return None


    def get_local_entries(self):
        if self.localbasepath != None:
            for path, dirs, files in os.walk(self.localbasepath):
                print("path:{0}".format(path))
                for name in files:
                    fullpath=os.path.join(path, name)
                    print(fullpath)


    def get_remote_entries(self, remotepath, result):
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
                        print(str(alldata, 'utf8'))

                    recved += str(alldata, 'utf8')

            dic = {}
            entries = []
            array = []
            for entry in recved.split('\n'):
                if entry is not '':
                    arr1=re.split(' .', entry)
                    print(arr1[0])
                    print(arr1[1])
                    print("===================================")

                    dic.update({arr1[1]:arr1[0]})

            for key, value in dic.items():
                print(key, value)

        else:
            print("Connection not opened.")


    def parse_config_file(self, config_file_path):
        config_file = open(config_file_path, 'r')
        config_json = json.loads(config_file.read())
        config_file.close()

        print(config_json)

        self.host = config_json['host']
        self.port = config_json['port']
        self.id = config_json['id']
        self.passwd = config_json['passwd']
        print(config_json['passwd'])
        print(config_json['local_base_path'])
        print(config_json['remote_base_path'])

        return

    def upload_file(self):
        return None


def main():
    print("Starting upload file.....")
    mode = None
    uploader = None

    if len(sys.argv) == 2:
        mode = 1
        config_file_path = sys.argv[1]
    elif len(sys.argv) == 3:
        mode = 2
        config_file_path = sys.argv[1]
        uploaded_file = sys.argv[2]
    else:
        print("the count of arguments was invalid.")
        return -1

    if os.path.exists(config_file_path) is False:
        print("config file was not existing")
        return -1

    if os.path.exists(config_file_path) is False:
        print("uploaded  not existing")
        return -1



    if mode is 1:
        uploader = sshuploader(config_file_path);

    elif mode is 2:
        uploader = sshuploader(config_file_path, uploaded_file);
        uploader.


if __name__ == "__main__":
    exit(main())







