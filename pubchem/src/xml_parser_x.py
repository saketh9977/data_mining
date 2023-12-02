from xml.etree import ElementTree as ET

import os
import json

def get_infodata(node, label, name=None, type_='sval'):
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
    if urn_label.text != label:
        return
    
    if name != None:
        urn_name = urn.find('PC-Urn_name')
        if urn_name is None:
            return
        if urn_name.text != name:
            return
    
    data_value = node.find('PC-InfoData_value')
    if data_value is None:
        return
    val = data_value.find(f'PC-InfoData_value_{type_}')
    if val is None:
        return
    return val.text

def parse_xml(in_filepath, out_folderpath):

    os.makedirs(out_folderpath, exist_ok=True)
    node_list = []
    node_data = {}
    for _, node in ET.iterparse(in_filepath):
        
        if '}' in node.tag:
            node.tag = node.tag.split('}')[-1]
        
        if node.tag == 'PC-Compound':
            node_list.append(node_data)
            node_data = {}

            # to-do: remove this
            if len(node_list) >= 2:
                break

        if node.tag == 'PC-CompoundType_id_cid':
            node_data['cid'] = node.text

        if node.tag == 'PC-Compound_charge':
            node_data['charge'] = node.text

        res = get_infodata(node, 'Compound Complexity', type_='fval')
        if res != None:
            node_data['compound_complexity'] = res

        res = get_infodata(node, 'Count', name='Hydrogen Bond Acceptor', type_='ival')
        if res != None:
            node_data['count_hydrogen_bond_acceptor'] = res

        res = get_infodata(node, 'Count', name='Hydrogen Bond Donor', type_='ival')
        if res != None:
            node_data['count_hydrogen_bond_donor'] = res

        res = get_infodata(node, 'Count', name='Rotatable Bond', type_='ival')
        if res != None:
            node_data['count_rotatable_bond'] = res

        res = get_infodata(node, 'Fingerprint', name='SubStructure Keys', type_='binary')
        if res != None:
            node_data['fingerprint_substructurekeys'] = res
        
        res = get_infodata(node, 'IUPAC Name', name='Allowed')
        if res != None:
            node_data['iupac'] = res
        
        res = get_infodata(node, 'InChI', name='Standard')
        if res != None:
            node_data['inchi'] = res
        
        res = get_infodata(node, 'InChIKey', name='Standard')
        if res != None:
            node_data['inchi_key'] = res

        res = get_infodata(node, 'Log P', type_='fval')
        if res != None:
            node_data['log_p'] = res

        res = get_infodata(node, 'Mass')
        if res != None:
            node_data['mass'] = res

        res = get_infodata(node, 'Molecular Formula')
        if res != None:
            node_data['molecular_formula'] = res

        res = get_infodata(node, 'Molecular Weight')
        if res != None:
            node_data['molecular_weight'] = res

        res = get_infodata(node, 'SMILES', name='Canonical')
        if res != None:
            node_data['smiles_canonical'] = res

        res = get_infodata(node, 'SMILES', name='Isomeric')
        if res != None:
            node_data['smiles_isomeric'] = res

        res = get_infodata(node, 'Topological', name='Polar Surface Area', type_='fval')
        if res != None:
            node_data['polar_surface_area'] = res

        res = get_infodata(node, 'Weight', name='MonoIsotopic')
        if res != None:
            node_data['weight_monoisotopic'] = res

        
            

    if len(node_data) != 0:
        node_list.append(node_data)

    out_filepath = os.path.join(out_folderpath, 'parsed.json')
    with open(out_filepath, 'w+') as out_stream:
        json.dump(node_list, out_stream, indent=4)