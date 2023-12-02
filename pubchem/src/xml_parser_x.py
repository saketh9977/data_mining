from xml.etree import ElementTree as ET

import os
import json

def get_iupac(node):
    if node.tag != 'PC-InfoData':
        return
    
    data_urn = node.find('PC-InfoData_urn')
    if data_urn is None:
        return
    urn = data_urn.find('PC-Urn')
    if urn is None:
        return
    urn_label = urn.find('PC-Urn_label')
    if urn_label is None:
        return
    if urn_label.text != 'IUPAC Name':
        return
    
    urn_name = urn.find('PC-Urn_name')
    if urn_name is None:
        return
    if urn_name.text != 'Allowed':
        return
    
    data_value = node.find('PC-InfoData_value')
    if data_value is None:
        return
    sval = data_value.find('PC-InfoData_value_sval')
    if sval is None:
        return
    return sval.text

def get_inchi_key(node):
    if node.tag != 'PC-InfoData':
        return
    
    data_urn = node.find('PC-InfoData_urn')
    if data_urn is None:
        return
    urn = data_urn.find('PC-Urn')
    if urn is None:
        return
    urn_label = urn.find('PC-Urn_label')
    if urn_label is None:
        return
    if urn_label.text != 'InChIKey':
        return
    
    urn_name = urn.find('PC-Urn_name')
    if urn_name is None:
        return
    if urn_name.text != 'Standard':
        return
    
    data_value = node.find('PC-InfoData_value')
    if data_value is None:
        return
    sval = data_value.find('PC-InfoData_value_sval')
    if sval is None:
        return
    return sval.text

def parse_xml(in_filepath, out_folderpath):

    os.makedirs(out_folderpath, exist_ok=True)
    node_list = []
    node_data = {}
    for _, node in ET.iterparse(in_filepath):
        
        if '}' in node.tag:
            node.tag = node.tag.split('}')[-1]
        

        if node.tag == 'PC-CompoundType_id_cid':
            if len(node_data) != 0:
                node_list.append(node_data)
            node_data = {}
            node_data['cid'] = node.text

        res = get_iupac(node)
        if res != None:
            node_data['iupac'] = res
        
        res = get_inchi_key(node)
        if res != None:
            node_data['inchi_key'] = res

    if len(node_data) != 0:
        node_list.append(node_data)

    out_filepath = os.path.join(out_folderpath, 'parsed.json')
    with open(out_filepath, 'w+') as out_stream:
        json.dump(node_list, out_stream, indent=4)