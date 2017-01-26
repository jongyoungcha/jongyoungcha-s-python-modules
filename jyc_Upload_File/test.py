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

    def __init__(self, host, port, id, passwd, localbasepath, remotebasepath):
        try:
            print("host:{0}".format(host))
            print("port:{0}".format(port))
            print("id:{0}".format(id))
            print("passwd:{0}".format(passwd))
            print("localbasepath:{0}".format(localbasepath))
            print("remotebasepath:{0}".format(remotebasepath))

            self.host = host
            self.port = port
            self.id = id
            self.passwd = passwd
            self.localbasepath = localbasepath
            self.remotebasepath = remotebasepath

            self.transport = paramiko.Transport((host, port))
            self.transport.connect(username = id, password = passwd)

            self.sftpclient = paramiko.SFTPClient.from_transport(self.transport)

        except SSHException("ssh connection error") as e:
            print(e)


    def connect_ssh(self):
        self.sshclient = paramiko.SSHClient()
        self.sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.sshclient.connect("192.168.120.82", 22, "root", "dusrn001")
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


    def parse_config_file(self):
        return


def main():
    print("main")
    uploader = None

    if len(sys.argv) == 1:
        config_file_path = argv[1]

    elif len(sys.argv) == 2:
        config_file_path = argv[1]
        uploaded_file = argv[2]

    else:
        print("the count of arguments was invalid.")
        return -1

    if os.path.exists(config_file_path) is False:
        print("config file was not existing")
        return -1

    if os.path.exists(config_file_path) is False:
        print("uploaded  not existing")
        return -1


    os.path.exists(config_file_path)

    uploader.get_local_entries();
    uploader.connect_ssh()


if __name__ == "__main__":
    exit(main())




    # if len(sys.argv) == 7:
    #     mode = sys.argv[0]
    #     host = sys.argv[1]
    #     port = sys.argv[2]
    #     id = sys.argv[3]
    #     passwd = argv[4]
    #     localbasepath = argv[5]
    #     remotebasepath = argv[6]
    #     uploader = sshuploader(host, port, id, passwd, localbasepath, remotebasepath)

    # elif len(sys.argv) == 8:
    #     mode = sys.argv[0]
    #     host = sys.argv[1]
    #     port = sys.argv[2]
    #     id = sys.argv[3]
    #     passwd = sys.argv[4]
    #     localbasepath = sys.argv[5]
    #     remotebasepath = sys.argv[6]
    #     uploadedfile = argv[7]
    #     uploader = sshuploader(host, port, id, passwd, localbasepath, remotebasepath, uploadedfile)
    # else:
    #     print("Arguments count was failed ( At least, please input 7 or 8 ). ")



