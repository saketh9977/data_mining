
from xml_parser_x import parse_xml

def main(args):
    print('main: starting...')
    parse_xml(args['in_filepath'], args['out_folderpath'])
    print('main: ending...')

if __name__ == '__main__':
    args = {
        # 'in_filepath': '../data/2.xml',
        # 'in_filepath': '../data/Compound_048500001_049000000.xml',
        'in_filepath': '../data/Compound_014000001_014500000.xml',
        'out_folderpath': '../out/'
    }
    main(args)