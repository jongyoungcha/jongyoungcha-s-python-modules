import sys
import paramiko
import os

class sshuploader:
    transport = None
    sshclient = None
    sftpclient = None
    host = None
    id = None
    passwd = None
    localbasepath = None
    remotebasepath = None
    uploadfile = None

    def __init__(self, host, port, id, passwd, localbasepath, remotebasepath, uploadfile):
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
            self.uploadfile = uploadfile


            self.transport = paramiko.Transport((host, port))
            self.transport.connect(username = id, password = passwd)

            self.sftpclient = paramiko.SFTPClient.from_transport(self.transport)

        except Exception("Fisrt ssh connection was failed..") as e:
            print(e)


    def connect_ssh(self):
        try:
            self.sshclient = paramiko.SSHClient()
            self.sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.sshclient.connect(self.host, self.port, self.id, self.passwd)
        except Exception("Connecting the remote server was failed...") as e:
            print(e)



    def disconnect_ssh(self):
        if sshclient:
            self.sshclient.close()

        return None



    def get_remote_entries(self):
        if(self.sshclient):
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



    def get_local_entries(self):
        if self.localbasepath != None:
            for path, dirs, files in os.walk(self.localbasepath):
                print("path:{0}".format(path))
                for name in files:
                    fullpath=os.path.join(path, name)
                    print(fullpath)

        return None

    def compare_entries(self):
        return None


    def upload_differ_entries(self):
        return None


    def compare_n_upload(self):
        return None



if __name__ == "__main__":
    print("main")

    mode=argv[0]
    host=argv[1]
    port=argv[2]
    id=argv[3]
    passwd=argv[4]
    local_path=argv[5]
    remote_path=argv[6]
    file_to_upload=argv[7]

    uploader = sshuploader(host, port, id, passwd, local_path, remote_path, file_to_upload)
    uploader.get_files_from_local()
    uploader.get_local_entries()
    uploader.connect_ssh()
    uplaoder.compa
    if mode is 1:
    else if mode is 2:
        return None
    else:
        return None




