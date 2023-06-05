from SSHClient import SSHClient
from SFTPClient import SFTPClient


def main():
    # List of destination systems
    destinations = [
        {"hostname": "192.168.56.101", "username": "kaushik", "password": "1234"}
    ]
    """
    source_path: path of directory present on remote system
    destination_path: path where the directory will be downloaded on local system
    """
    source_path = "C:/12345"
    destination_path = "C:/Users/kaushik/Documents/Python/Data-Copy-Auto/Test"

    # Operation
    for destination in destinations:
        # Create ssh connection
        ssh_connection = SSHClient(
            destination["hostname"], destination["username"], destination["password"]
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
