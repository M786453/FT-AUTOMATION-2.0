import paramiko
from Popup import Popup
import os

class SSHClient:

    """
    This function is used for initializing variables
    """

    def __init__(self, hostname, username, password, port=22):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = port
        self.client = paramiko.SSHClient()
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    """
    This function will help the local system to connect with target ssh server
    """

    def connect(self):
        try:
            self.client.connect(
                self.hostname,
                port=self.port,
                username=self.username,
                password=self.password,
            )
            return True
        except paramiko.AuthenticationException:
            print("Authentication failed for", self.hostname)
        except paramiko.SSHException as ssh_exc:
            print("SSH error:", str(ssh_exc), "for", self.hostname)
        except Exception as e:
            print("Error:", str(e), "for", self.hostname)
        return False

    """
    This function will help the local system to disconnect from target ssh server
    """

    def disconnect(self):
        self.client.close()

    """
    Shutdown remote system
    """
    def shutdownRemoteSys(self):
        # Execute the shutdown command
        command = "shutdown /s /f /t 0"
        print("\033[33mShutting Down Remote System.\033[0m")
        Popup.show(self.hostname, "Shutting Down System.",15000)
        self.client.exec_command(command)

    
    """
    Shutdown local system
    """
    def shutdownLocalSys(self):
        
        print("\033[33mShutting Down Local System.\033[0m")
        Popup.show("Local System", "Shutting Down System.",15000)    
        os.system("shutdown /s /t 0")





