from SSHClient import SSHClient
from SFTPClient import SFTPClient
from Popup import Popup
def main():

    hostname = "192.168.222.129"
    username = "Ahtesham Sarwar"
    password = "1234"
    

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
            sftp_client.upload_directory(source_path, destination_path)
        finally:
            # shutdown local system
            ssh_connection.shutdownLocalSys()
            # close ssh connection
            ssh_connection.disconnect()

if __name__ == "__main__":
    main()
