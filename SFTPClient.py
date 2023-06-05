import os
import stat 


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
                
                log = "'" + remote_path + "' downloaded."
                self.logs += log + "\n"

                # Print coloured output using ANSI sequence
                # Using green color to print downloaded files logs
                print("\033[1;32m" + log + "\033[0m" )

        except Exception as e:
            print("Error:", str(e), "for", self.hostname)
        finally:
            sftp.close()

    def _write_logs(self):
        with open("logs.txt", "w") as logFile:
            logFile.write(self.logs)

