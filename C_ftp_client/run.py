#!/usr/bin/python3.6
from datetime import datetime, timezone, timedelta
import ftplib
import os

base_dir = "/var/sentry.d"
# base_dir = os.path.dirname(os.path.abspath(__file__))     # current file path, use this if you want to save file here

server_address = "127.0.0.1"


if __name__ == "__main__":
    ftp = ftplib.FTP()
    ftp.connect(server_address, 21)
    ftp.login()
    ftp.cwd(base_dir)

    # if directory does not exist,
    now = datetime.now(tz=timezone(timedelta(hours=9)))
    if not os.path.exists(f"{base_dir}/{now.strftime('%Y-%m-%d')}"):
        os.makedirs(f"{base_dir}/{now.strftime('%Y-%m-%d')}", mode=0o777)

    with open(f"{base_dir}/{now.strftime('%Y-%m-%d')}/{now.strftime('%Y%m%d-%H%M%S')}.csv", "w", ) as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        for row in results:
            writer.writerow(row)

    try:
        dir_or_files = ftp.nlst()
    except ftplib.Error as e:
        e

    with open("./" + filename, "wb") as f:
        ftp.retrbinary("RETR " + filename, f.write)
