from xml.etree import cElementTree as ET

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

def clear_nodes(nodes_to_clear):

    """
        remove nodes from memory (RAM)
    """

    for node in nodes_to_clear:
        node.clear()

def parse_xml(args):

    """
        11.2 MB peak Memory usage for 580 MB xml
        30 MB peak Memory usage for 4.7 GB xml (2m 15s runtime)
            parsed_node_list is written to disk every batch of 100 records
    """

    parsed_node_list = []
    parsed_node_dict = {}
    nodes_to_clear = []
    for _, node in ET.iterparse(args['in_filepath']):
        
        if '}' in node.tag:
            node.tag = node.tag.split('}')[-1]
        
        if node.tag == 'PC-Compound':
            parsed_node_list.append(parsed_node_dict)
            parsed_node_dict = {}
            clear_nodes(nodes_to_clear)
            nodes_to_clear = []

            if len(parsed_node_list) >= args['batch_size']:
                yield parsed_node_list
                parsed_node_list = []

            # to-do: remove this
            # if len(parsed_node_list) >= 2:
            #     break

        elif node.tag == 'PC-CompoundType_id_cid':
            parsed_node_dict['cid'] = node.text

        elif node.tag == 'PC-Compound_charge':
            parsed_node_dict['charge'] = node.text

        elif node.tag == 'PC-InfoData':
            res = get_infodata(node, 'Compound Complexity', type_='fval')
            if res != None:
                parsed_node_dict['compound_complexity'] = res

            res = get_infodata(node, 'Count', name='Hydrogen Bond Acceptor', type_='ival')
            if res != None:
                parsed_node_dict['count_hydrogen_bond_acceptor'] = res

            res = get_infodata(node, 'Count', name='Hydrogen Bond Donor', type_='ival')
            if res != None:
                parsed_node_dict['count_hydrogen_bond_donor'] = res

            res = get_infodata(node, 'Count', name='Rotatable Bond', type_='ival')
            if res != None:
                parsed_node_dict['count_rotatable_bond'] = res

            res = get_infodata(node, 'Fingerprint', name='SubStructure Keys', type_='binary')
            if res != None:
                parsed_node_dict['fingerprint_substructurekeys'] = res
            
            res = get_infodata(node, 'IUPAC Name', name='Allowed')
            if res != None:
                parsed_node_dict['iupac'] = res
            
            res = get_infodata(node, 'InChI', name='Standard')
            if res != None:
                parsed_node_dict['inchi'] = res
            
            res = get_infodata(node, 'InChIKey', name='Standard')
            if res != None:
                parsed_node_dict['inchi_key'] = res

            res = get_infodata(node, 'Log P', type_='fval')
            if res != None:
                parsed_node_dict['log_p'] = res

            res = get_infodata(node, 'Mass')
            if res != None:
                parsed_node_dict['mass'] = res

            res = get_infodata(node, 'Molecular Formula')
            if res != None:
                parsed_node_dict['molecular_formula'] = res

            res = get_infodata(node, 'Molecular Weight')
            if res != None:
                parsed_node_dict['molecular_weight'] = res

            res = get_infodata(node, 'SMILES', name='Canonical')
            if res != None:
                parsed_node_dict['smiles_canonical'] = res

            res = get_infodata(node, 'SMILES', name='Isomeric')
            if res != None:
                parsed_node_dict['smiles_isomeric'] = res

            res = get_infodata(node, 'Topological', name='Polar Surface Area', type_='fval')
            if res != None:
                parsed_node_dict['polar_surface_area'] = res

            res = get_infodata(node, 'Weight', name='MonoIsotopic')
            if res != None:
                parsed_node_dict['weight_monoisotopic'] = res
        
        nodes_to_clear.append(node)
                

    if len(parsed_node_list) != 0:
        yield parsed_node_list