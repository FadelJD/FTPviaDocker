import os
import time
from ftplib import FTP
from prometheus_client import start_http_server, Gauge
from flask import Flask, Response

app = Flask(__name__)

ftp_files_count = Gauge('ftp_files_count', 'Number of files in the FTP server')
ftp_total_size = Gauge('ftp_total_size', 'Total size of files in the FTP server')
ftp_txt_files_count = Gauge('ftp_txt_files_count', 'Number of files containing "txt" in their name')
ftp_mp3_files_count = Gauge('ftp_mp3_files_count', 'Number of files containing "mp3" in their name')
ftp_jpg_files_count = Gauge('ftp_jpg_files_count', 'Number of files containing "jpg" or "jpeg" in their name')
ftp_files_uploaded = Gauge('ftp_files_uploaded', 'Number of files uploaded to the FTP server')
ftp_files_downloaded = Gauge('ftp_files_downloaded', 'Number of files downloaded from the FTP server')

FTP_HOST = '127.0.0.1'
FTP_PORT = 21
FTP_USER = 'ahmed'
FTP_PASS = '1234'

def update_metrics():
    try:
        ftp = FTP()
        ftp.connect(FTP_HOST, FTP_PORT)
        ftp.login(FTP_USER, FTP_PASS)
        files = ftp.nlst()

        ftp_files_count.set(len(files))

        files_total_size = 0
        txt_files_count = 0
        mp3_files_count = 0
        jpg_files_count = 0

        for file in files:
            try:
                file_size = ftp.size(file)
            except Exception:
                continue

            files_total_size += file_size

            if "txt" in file:
                txt_files_count += 1
            if "mp3" in file:
                mp3_files_count += 1
            if "jpg" in file or "jpeg" in file:
                jpg_files_count += 1

        ftp_total_size.set(files_total_size)
        ftp_txt_files_count.set(txt_files_count)
        ftp_mp3_files_count.set(mp3_files_count)
        ftp_jpg_files_count.set(jpg_files_count)

        ftp.quit()

    except Exception as e:
        print(f"Error updating metrics: {e}")

@app.route('/metrics')
def metrics():
    update_metrics()
    return Response("\n".join([
        ftp_files_count.generate_latest().decode('utf-8'),
        ftp_total_size.generate_latest().decode('utf-8'),
        ftp_txt_files_count.generate_latest().decode('utf-8'),
        ftp_mp3_files_count.generate_latest().decode('utf-8'),
        ftp_jpg_files_count.generate_latest().decode('utf-8'),
        ftp_files_uploaded.generate_latest().decode('utf-8'),
        ftp_files_downloaded.generate_latest().decode('utf-8')
    ]), content_type='text/plain; version=0.0.4; charset=utf-8')

if __name__ == '__main__':
    start_http_server(8000)
    while True:
        update_metrics()
        time.sleep(5)
