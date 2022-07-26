import ftplib
import io
from datetime import datetime
from os import path
from os import makedirs
import pandas as pd


class ProviderFTP(object):
    """
    Provider FTP Class
    """    
    def __init__(self, server, user, password):
        """
        Init the Class

        Args:
            server (str): ftp server
            user (str): ftp user
            password (str): ftp password
        """        
        self.server = server
        self.user = user
        self.password = password
        dir_project = path.dirname(path.abspath(__file__))
        self.download = datetime.now().strftime('%Y%m')
        self.dir_download = f'{dir_project}/download'


    def connect_ftp_server(self):
        """
        Connect FTP Server
        """
        print(f"Starting at {datetime.now().strftime('%Y-%m-%d %Hh%Mm%S')}")
        try:
            self.ftp = ftplib.FTP(self.server)
            self.ftp.login(self.user, self.password)
            print('Connected on FTP')

        except Exception as e:
            print(e)
            self.ftp = None

    def get_files(self):
        """
        Search the files to download
        """        
        self.files = list(filter(lambda x: '.CSV' in x, self.ftp.nlst(self.download)))

    def save_files(self):
        """
        Retrieve data from FTP server and save in files on diretory
        """
        
        makedirs(f'{self.dir_download}/{self.download}', exist_ok=True)

        self.get_max_files()
        
        print(f'Files to download: {self.files}', end='\n')

        for file in self.files:
            try:
                r = io.BytesIO()
                self.ftp.retrbinary('RETR /'+ file, r.write)

                data = r.getvalue().decode()
                f = open(f'{self.dir_download}/{file}' , 'w+')
                f.write(data)
                f.close()
            
                r.close()
            except:
                pass