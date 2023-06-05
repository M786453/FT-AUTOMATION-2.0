from SSHClient import SSHClient
from SFTPClient import SFTPClient



def main():

    hostname = input("Enter Hostname: ")
    username = input("Enter Username: ")
    password = input("Enter Password: ")

    """
    source_path: path of directory present on remote system
    destination_path: path where the directory will be downloaded on local system
    """
    source_path = "E:/123"
    destination_path = "./"


    ssh_connection = SSHClient(
            hostname, username, password
        )

    if ssh_connection.connect():  # connection successful
        try:
            sftp_client = SFTPClient(ssh_connection)
            sftp_client.download_directory(source_path, destination_path)
        finally:
            # close ssh connection
            ssh_connection.disconnect()

if __name__ == "__main__":
    main()
