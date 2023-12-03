import json
import os, shutil
from datetime import datetime, timedelta

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

if __name__ == '__main__':
    print_x('34')
    print_x('test')
