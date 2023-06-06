import os
import stat 
from datetime import datetime

class SFTPClient:
    def __init__(self, ssh_connection):
        self.ssh_connection = ssh_connection
        self.logs = ""

    """
    This function is used to download a directory from remote server into local system.
    """

    def download_directory(self, source_path, destination_path):
        parent_down_dir = os.path.basename(
            source_path
        )  # parent downloading directory name
        self.root_path = os.path.join(destination_path, parent_down_dir)
        self._download(source_path, self.root_path)
        self._write_logs()
        


    """
    This function is the part of 'download_directory' function.
    """

    def _download(self, source_path, destination_path):
        sftp = self.ssh_connection.client.open_sftp()

        try:
            try:
                os.makedirs(destination_path)
            except Exception:
                print("'" + destination_path + "'", "directory already exists.")
                # in order to avoid stopping of downloading process if parent directory already exists
                if destination_path != self.root_path:
                    return

            for item in sftp.listdir_attr(source_path): # Recursive directory download
                remote_path = os.path.join(source_path, item.filename)
                local_path = os.path.join(destination_path, item.filename)

                if stat.S_ISDIR(item.st_mode):  # Check if it's a directory
                    self._download(remote_path, local_path)
                else:
                    # If file not exists in local system, then download it
                    if not os.path.exists(local_path):
                        sftp.get(remote_path, local_path)
                
                self._logging(remote_path, "downloaded")

        except Exception as e:
            print("Error:", str(e), "for", self.hostname)
        finally:
            sftp.close()


    """
    This function is used to upload a directory from local system to remote server.
    source_path: path of directory present on local system
    destination_path: path where the directory will be uploaded on remote server
    """
    def upload_directory(self, source_path, destination_path):

        sftp = self.ssh_connection.client.open_sftp()

        existing_dirs = []

        try:

            parent_src_dir_name = os.path.basename(os.path.normpath(source_path)) # name of source's parent directory
        
            parent_destination_dir = os.path.join(destination_path, parent_src_dir_name)

            try:
                sftp.mkdir(parent_destination_dir)
            except Exception as e:
                print("'" + parent_src_dir_name + "'", "directory already exists.")
                
            
            for root, dirs, files in os.walk(source_path):
                
                
                for dir in dirs:
                    local_path = os.path.join(root, dir)
                    relative_path = os.path.relpath(local_path, source_path)
                    remote_path = os.path.join(parent_destination_dir, relative_path)
                    try:
                        sftp.mkdir(remote_path)
                        self._logging(local_path, "uploaded")
                    except Exception as e:
                        existing_dirs.append(os.path.normpath(local_path))
                        print("'" + dir + "'", "directory already exists.")


                # in order to avoid uploading files to a directory which already exists
                if os.path.normpath(root) in existing_dirs:
                    continue

                for file in files:
                    local_path = os.path.join(root, file)
                    relative_path = os.path.relpath(local_path, source_path)
                    remote_path = os.path.join(parent_destination_dir, relative_path)
                    try:
                        if not self._file_exists(sftp, remote_path):
                            sftp.put(local_path, remote_path)
                            self._logging(local_path, "uploaded")
                        else:
                            print(file, "file already exists.")      
                    except Exception as e:
                        print("Error copying file:", str(e), "for", self.hostname)
            
            self._write_logs()

        except Exception as e:
            print("Error:", str(e), "for", self.hostname)
        finally:
            sftp.close()


    """
    This function checks whether the specified file exists or not on remote server
    """
    def _file_exists(self, sftp, remote_path):
        try:
            sftp.stat(remote_path)
            return True # File exists
        except FileNotFoundError:
            return False # File does not exists
        


    def _write_logs(self):
        with open("logs.txt", "w") as logFile:
            logFile.write(self.logs)

    def _logging(self, path, status):

        log = "'" + path + f"' {status}. [ " + str(datetime.now()) + " ]"
        self.logs += log + "\n"

        # Print coloured output using ANSI sequence
        # Using green color to print downloaded files logs
        print("\033[1;32m" + log + "\033[0m" )

