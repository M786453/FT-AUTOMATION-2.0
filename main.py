from SSHClient import SSHClient
from SFTPClient import SFTPClient
import getpass


def main():

    hostname = input("Enter Hostname: ")
    username = input("Enter Username: ")
    password = getpass.getpass("Enter Password: ")
    
    print("Entered Password:", "*"*len(password))

    """
    source_path: path of directory present on remote system
    destination_path: path where the directory will be downloaded on local system
    """
    source_path = input("Enter Source Path: ")
    destination_path = input("Enter Destination Path: ")

    ssh_connection = SSHClient(
            hostname, username, password
        )

    if ssh_connection.connect():  # connection successful
        try:
            sftp_client = SFTPClient(ssh_connection)
            sftp_client.download_directory(source_path, destination_path)
        finally:
            # shutdown remote system
            ssh_connection.shutdownRemoteSys()
            # close ssh connection
            ssh_connection.disconnect()

if __name__ == "__main__":
    main()
