
from xml_parser_x import parse_xml
from utils_x import write_to_json, remove_dir, print_x

import os

def main(args):
    print_x('main: starting...')

    remove_dir(args['out_folderpath'])
    os.makedirs(args['out_folderpath'], exist_ok=True)

    f_args = {
        'in_filepath': args['in_filepath'],
        'batch_size': int(args['out_json_batch_size'])
    }
    out_filepath = os.path.join(args['out_folderpath'], 'parsed.json')
    for parsed_batch in parse_xml(f_args):
        write_to_json(parsed_batch, out_filepath)

    print_x('main: ending...')

if __name__ == '__main__':
    args = {
        # 'in_filepath': '../data/2.xml',
        # 'in_filepath': '../data/Compound_048500001_049000000.xml',
        'in_filepath': '../data/Compound_014000001_014500000.xml',
        'out_json_batch_size': '100',
        'out_folderpath': '../out/'
    }
    main(args)