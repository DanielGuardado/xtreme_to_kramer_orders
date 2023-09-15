from ftplib import FTP
import os
from config import ftp_data


class FTPUploader:
    def __init__(self, host, username, password, dest_path, port=21):
        self.host = host
        self.username = username
        self.password = password
        self.dest_path = dest_path
        self.port = port

    def upload_file(self, file_path):
        """
        Uploads a file to the FTP server.

        :param file_path: The local path of the file to be uploaded.
        """
        with FTP() as ftp:
            # Connect to the server
            ftp.connect(host=self.host, port=self.port)
            ftp.login(user=self.username, passwd=self.password)

            # Change to the appropriate directory (if specified in dest_path)
            if "/" in self.dest_path:
                directory = "/".join(self.dest_path.split("/")[:-1])
                ftp.cwd(directory)

            # Upload the file
            with open(file_path, "rb") as file:
                ftp.storbinary(f"STOR {self.dest_path.split('/')[-1]}", file)

            print(f"{file_path} uploaded successfully to {self.dest_path}")

    @staticmethod
    def from_config(filename):
        file_ending = os.path.basename(filename)
        return FTPUploader(
            ftp_data["host"],
            ftp_data["username"],
            ftp_data["password"],
            f"{ftp_data['dest_path']}/{file_ending}",
        )
