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
    config_file_path = None
    localbasepath = None
    remotebasepath = None
    uploaded_file = None
    remote_file = None

    def __init__(self, config_file_path, uploaded_file):
        try:
            # Check file was existing
            self.config_file_path = config_file_path
            if os.path.exists(config_file_path) is None:
                return None

            self.uploaded_file = uploaded_file
            print("uploaded file : {0}".format(self.uploaded_file))

            # Parse config
            if self.parse_config_file(config_file_path) == False:
                print('>>>>parse_config_file() was failed...')
                sys.exit()

            # Connect to server
            self.transport = paramiko.Transport((self.host, int(self.port)))
            self.transport.connect(username=self.id, password=self.passwd)
            self.connect_ssh();

            if self.check_config() == False:
                print('>>>>check_config() was failed...')

        except SSHException("ssh connection error") as e:
            print(e)

        except ssh_exception.AuthenticationException as e:
            print(e)


    def check_config(self):
        print(">>>> In check_config()")
        # check remote base path
        ret = True
        if not os.path.exists(self.localbasepath):
            print("local base path is not exists.")
            return ret

        # check local base path
        try:
            self.sftpclient.stat(self.remotebasepath)
        except IOError as e:
            # print("No such file{0}", str(e))
            return False

        # check upload file path
        if self.uploaded_file.find(self.localbasepath) is -1:
            return False
        else:
            relative_path = self.uploaded_file.replace(self.localbasepath, "")

        # set remote path
        self.remote_file = "{0}/{1}".format(self.remotebasepath, relative_path)
        print(self.remote_file)

        return True


    def connect_ssh(self):
        self.sshclient = paramiko.SSHClient()
        self.sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.sshclient.connect(self.host, self.port, self.id, self.passwd)

        self.sftpclient = paramiko.SFTPClient.from_transport(self.transport)
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
        print(">>>> In parse_config_file()")

        config_file = open(config_file_path, 'r')
        config_json = json.loads(config_file.read())
        config_file.close()

        self.host = config_json['host']
        self.port = int(config_json['port'])
        self.id = config_json['id']
        self.passwd = config_json['passwd']
        self.localbasepath = os.path.dirname(self.config_file_path)
        if self.localbasepath == '.' :
            self.localbasepath = os.getcwd()

        self.remotebasepath = config_json['remote_base_path']

        print("host : {0}".format(self.host))
        print("port : {0}".format(self.port))
        print("id : {0}".format(self.id))
        print("passwd : {0}".format(self.passwd))
        print("remotepath : {0}".format(self.remotebasepath))
        print("localbaseapth : {0}".format(self.localbasepath))

        return None

    
    def upload_file(self):
        if (self.uploaded_file):
            self.uploaded_file = self.uploaded_file.replace("."+os.sep, self.localbasepath+os.sep)

        self.remote_file = "{0}/{1}".format(self.remotebasepath, self.uploaded_file.replace(self.localbasepath, ""))

        print(">>>> Uploading local_path{0} ||||| remote_path : {1}".format(self.uploaded_file, self.remote_file))

        self.sftpclient.put(self.uploaded_file, self.remote_file)


        return None


def main():
    print("Starting upload file.....")
    mode = None
    uploader = None
    uploaded_file = None

    print(sys.argv[0])
    print(sys.argv[1])
    print(sys.argv[2])


    if len(sys.argv) == 2:
        mode = 1
        config_file_path = sys.argv[1]
    elif len(sys.argv) == 3:
        mode = 2
        config_file_path = sys.argv[1]
        uploaded_file = sys.argv[2]
        print("loaded file :",uploaded_file)
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
        print(">>>>> this mode is directoy compare")
        uploader = sshuploader(config_file_path)
    elif mode is 2:
        print(">>>>> this mode is file uploader")
        uploader = sshuploader(config_file_path, uploaded_file)
        uploader.upload_file()


if __name__ == "__main__":
    exit(main())







