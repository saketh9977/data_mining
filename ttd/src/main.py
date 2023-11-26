import re
import os
import json
from datetime import datetime

from utils_x import print_x

def parse_drug_disease_mapping(args):
    
    """
        1. Drug to disease -> 1 to many mapping 
    """

    drug_disease_mapping = {}
    with open(args['in_filepath'], 'r') as in_stream:

        ttd_drug_id = None
        for ind, line in enumerate(in_stream):
            
            if (ind+1) < args['data_start_from_line']:
                continue

            line = line.strip()

            if line == '':
                ttd_drug_id = None

            token_list = line.split('\t')
            if token_list[0] == 'TTDDRUID':
                ttd_drug_id = token_list[1]
                if (ttd_drug_id in drug_disease_mapping) == False:
                    drug_disease_mapping[ttd_drug_id] = {}
            
            if token_list[0] == 'DRUGNAME':
                drug_disease_mapping[ttd_drug_id]['ttd_drug_name'] = token_list[1]
            
            if token_list[0] == 'INDICATI':
                if ('ttd_disease' in drug_disease_mapping[ttd_drug_id]) == False:
                    drug_disease_mapping[ttd_drug_id]['ttd_disease'] = []

                match = re.search(r'(.*?)\s*\[.*?\]', token_list[1])
                if match:
                    ttd_disease = match.group(1).strip()
                                
                match = re.search(r'\[.*?\]', token_list[1])
                if match:
                    icd11 = match.group(0).strip()[1:-1]

                match = re.search(r'\[.*?\]\s*(.*)', token_list[1])
                if match:
                    clinical_status = match.group(1).strip()

                drug_disease_mapping[ttd_drug_id]['ttd_disease'].append({
                    'ttd_disease_name': ttd_disease,
                    'icd11': icd11,
                    'clinical_status': clinical_status,
                    'updated_at': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
                })

            
    out_filepath = os.path.join(args['out_dir_path'], 'drug_disease_mapping.json')
    with open(out_filepath, 'w+') as out_stream:
        json.dump(drug_disease_mapping, out_stream, indent=4)

def parse_biomarker_disease_mapping(args):

    biomarker_disease_mapping = {}
    with open(args['in_filepath'], 'r') as in_stream:
        
        for ind, line in enumerate(in_stream):
            if (ind+1) < args['data_start_from_line']:
                continue
            
            line = line.strip()
            if line == '':
                continue

            token_list = line.split('\t')            
            biomarker_id = token_list[0]
            biomarker_name = token_list[1]
            disease_name = token_list[2]
            icd11 = token_list[3]

            if (biomarker_id in biomarker_disease_mapping) == False:
                biomarker_disease_mapping[biomarker_id] = []

            biomarker_disease_mapping[biomarker_id].append({
                'ttd_biomarker_name': biomarker_name,
                'ttd_disease_name': disease_name,
                'icd11': icd11
            })

    out_filepath = os.path.join(args['out_dir_path'], 'biomarker_disease_mapping.json')
    with open(out_filepath, 'w') as out_stream:
        json.dump(biomarker_disease_mapping, out_stream, indent=4)

def parse_drug_info(args):

    prop_to_label_mapping = {
        'DRUG__ID':	'ttd_drug_id',
        'TRADNAME':	'drug_trade_name',
        'DRUGCOMP':	'drug_company',
        'THERCLAS':	'drug_therapeutic_class',
        'DRUGTYPE':	'drug_type',
        'DRUGINCH':	'inchi',
        'DRUGINKE':	'inchi_key',
        'DRUGSMIL':	'canonical_smiles',
        'HIGHSTAT':	'highest_status',
        'DRUGCLAS':	'drug_class',
        'DRUADIID': 'adi_id',
        'COMPCLAS':	'compound_class'
    }
    drug_info = {}

    with open(args['in_filepath'], 'r') as in_stream:

        for ind, line in enumerate(in_stream):
            if (ind+1) < args['data_start_from_line']:
                continue

            line = line.strip()
            if line == '':
                continue

            token_list = line.split('\t')
            ttd_drug_id = token_list[0]
            drug_prop = token_list[1]
            prop_value = token_list[2]

            label = prop_to_label_mapping[drug_prop]
            if (ttd_drug_id in drug_info) == False:
                drug_info[ttd_drug_id] = {}

            drug_info[ttd_drug_id][label] = prop_value.strip()

    out_file_path = os.path.join(args['out_dir_path'], 'drug_info.json')
    with open(out_file_path, 'w+') as out_stream:
        json.dump(drug_info, out_stream, indent=4)


def main(args):
    print_x("main: starting...")

    os.makedirs(args['out_dir_path'], exist_ok=True)
    
    # f_args = {
    #     'in_filepath': os.path.join(args['data_dir_path'], 'P1-05-Drug_disease.txt'),
    #     'data_start_from_line': int(args['drug_disease_mapping_data_start_line']),
    #     'out_dir_path': args['out_dir_path']
    # }
    # parse_drug_disease_mapping(f_args)

    # f_args = {
    #     'in_filepath': os.path.join(args['data_dir_path'], 'P1-08-Biomarker_disease.txt'),
    #     'data_start_from_line': int(args['biomarker_disease_mapping_data_start_line']),
    #     'out_dir_path': args['out_dir_path']
    # }
    # parse_biomarker_disease_mapping(f_args)

    f_args = {
        'in_filepath': os.path.join(args['data_dir_path'], 'P1-02-TTD_drug_download.txt'),
        'data_start_from_line': int(args['drug_info_start_line']),
        'out_dir_path': args['out_dir_path']
    }
    parse_drug_info(f_args)

    print_x("main: ending...")

if __name__ == '__main__':

    args = {
        'data_dir_path': '../data',
        'drug_disease_mapping_data_start_line': '23',
        'biomarker_disease_mapping_data_start_line': '17',
        'drug_info_start_line': '30',
        'out_dir_path': '../out'
    }

    main(args)