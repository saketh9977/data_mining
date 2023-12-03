import json
import os, shutil
from datetime import datetime, timedelta
import ftplib

def print_x(data):
    timestamp_str = (datetime.utcnow() + timedelta(hours=5, minutes=30)).strftime('%Y-%m-%d %H:%M:%S IST')
    print(f"{timestamp_str} -> {data}")

def remove_dir(dir_path):
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)

def write_to_json(data_list, out_filepath):

    with open(out_filepath, 'a+') as out_stream:
        for data_dict in data_list:
            json.dump(data_dict, out_stream)
            out_stream.write('\n')

def list_ftp_files(ftp_url):

    out = []
    parts = ftp_url.split("/")
    server = parts[2]
    path = "/".join(parts[3:])

    with ftplib.FTP(server) as ftp:
        ftp.login()
        ftp.cwd(path)
        files = ftp.nlst()
        for file in files:
            if file.endswith('.gz'):
                out.append(file)

    return out


if __name__ == '__main__':
    ftp_url = "https://ftp.ncbi.nlm.nih.gov/pubchem/Compound/CURRENT-Full/XML"
    list_ftp_files(ftp_url)
