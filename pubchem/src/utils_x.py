import json
import os, shutil
from datetime import datetime, timedelta
import ftplib
import csv

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

    """
        example: "https://ftp.ncbi.nlm.nih.gov/pubchem/Compound/CURRENT-Full/XML"
    """

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

def get_csv_from_json(in_json_path, out_csv_path):

    csv_2d_list = []
    header_row = []
    with open(in_json_path, 'r') as in_stream:
        for ind, line in enumerate(in_stream):
            if line.strip() == '':
                continue
            line_dict = json.loads(line)

            if ind == 0:
                for key in line_dict:
                    header_row.append(key)

            row = []
            for key in header_row:
                row.append(line_dict[key])
            csv_2d_list.append(row)

    with open(out_csv_path, 'w+') as out_stream:
        csv_writer = csv.writer(out_stream)
        csv_writer.writerows(csv_2d_list)

if __name__ == '__main__':
    in_json_path = '../out/2.json'
    out_csv_path = '../out/2.csv'
    get_csv_from_json(in_json_path, out_csv_path)
