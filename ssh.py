import paramiko
from paramiko import SSHException
import logger


class SshConnection:
    def __init__(self,ipaddress,port,username,password):
        self.client = None
        self.ipaddress = ipaddress
        self.port = port
        self.username = username    
        self.password = password

    def is_connected(self):
        try:
            transport = self.client.get_transport()
            transport.send_ignore()
            return True
        except EOFError as e:
            return False


    def connect(self):
        logger.info(f"Attempting to connect to {self.ipaddress} ...")
        self.client=paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(self.ipaddress,self.port,self.username,self.password)


    def send_command(self,command):
        try:
            stdin, stdout, stderr = self.client.exec_command(command)
            stdout=stdout.readlines()
            return stdout
        except SSHException as e:
            logger.error(repr(e))


if __name__ == "__main__":
    pass