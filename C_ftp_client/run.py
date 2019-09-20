#!/usr/bin/python3.6
from datetime import datetime, timezone, timedelta
import ftplib
import os


host = "127.0.0.1"
port = 21
username = "sentry02"
password = "teknone!"

source_dir = "/var/sentry.d"
destination_dir = "/home/sentry02/Downloads/sentry/"


def main():
    # get current time as KST
    now = datetime.now(tz=timezone(timedelta(hours=9)))

    # ftp connect and login
    ftp = ftplib.FTP()
    ftp.connect(host=host, port=port)
    ftp.login(user=username, passwd=password)

    # move current working directory to source_dir
    ftp.cwd(source_dir)

    # linux command ls results on ftp server cwd(source_dir)
    src_dir_or_files = ftp.nlst()

    # linux command ls results on destination_dir path
    dst_dir_or_files = os.listdir(destination_dir)

    # get target to download
    download_target = set(src_dir_or_files) - set(dst_dir_or_files)

    # download files from source_dir of ftp server to destination_dir
    for dir_or_file in download_target:
        try:
            with open(f"{destination_dir}/{dir_or_file}", "wb") as f:
                ftp.retrbinary(f"RETR {dir_or_file}", f.write)
        except ftplib.Error as e:
            if os.path.exists(f"{destination_dir}/{dir_or_file}"):
                os.remove(f"{destination_dir}/{dir_or_file}")


if __name__ == "__main__":
    main()
