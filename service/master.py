from collections import defaultdict
from lxml import etree
from service import create_master as cm

import pandas as pd


def tag_master(loc, ct, fn, sn):
    df = pd.read_excel(f'{loc}/{ct}/excel/{fn}.xlsx', sheet_name=sn)
    df.sort_values(by=['Has Content'], ascending=False, inplace=True)
    df.drop_duplicates(subset=['Tags'], inplace=True)
    df = df[['Tags', 'Has Content']]
    df.rename({'Tags': 'tag', 'Has Content': 'has_text'}, axis=1, inplace=True)
    with pd.ExcelWriter(f'{loc}/{ct}/excel/{ct}_rule.xlsx', engine='openpyxl', mode='a',
                        if_sheet_exists='replace') as writer:
        df.to_excel(writer, sheet_name='tag_master', index=False)
    return True


ct = ''
pc_dic = {}
att_dic = {}
file_name = ''
prod_name = ''


def xml_traverse_att(root):
    tag_name = etree.QName(root).localname
    for key, val in root.attrib.items():
        key = etree.QName(key).localname
        my_id = f'{tag_name}_{key}'
        if my_id not in att_dic:
            att_dic[my_id] = (my_id, tag_name, key, val, file_name, prod_name, ct)

    for child in root:
        if type(child) == etree._Element:
            xml_traverse_att(child)


def xml_traverse_pc(root):
    my_ls = []
    for child in root:
        if type(child) == etree._Element:
            child_name = etree.QName(child).localname
            my_ls.append(child_name)
            xml_traverse_pc(child)
    tag_name = etree.QName(root).localname

    counter = defaultdict(int)
    for letter in my_ls:
        counter[letter] += 1
    res = tag_name + '=>'
    for k, v in counter.items():
        res += f'_{k}({str(v)})'

    pc_dic[res] = (res, tag_name, file_name, prod_name, ct)


def process_master(loc, content_type, all_dir, products, master_type):
    global att_dic, pc_dic, file_name, prod_name, ct
    ct = content_type

    if master_type == 'att':
        for root, f_name, p_name in cm.get_xml_root(loc, content_type, all_dir, products):
            file_name = f_name
            prod_name = p_name
            xml_traverse_att(root)
        df = pd.DataFrame(att_dic.values(), columns=['id', 'tag', 'key', 'val', 'file_name', 'prod_name', 'ct'])
        # df.drop('column_name', axis=1, inplace=True)
        with pd.ExcelWriter(f'{loc}/{ct}/excel/{ct}_rule.xlsx', engine='openpyxl', mode='a',
                            if_sheet_exists='replace') as writer:
            df.to_excel(writer, sheet_name='att_master', index=False)
        att_dic = {}

    elif master_type == 'pc':
        for root, f_name, p_name in cm.get_xml_root(loc, content_type, all_dir, products):
            file_name = f_name
            prod_name = p_name
            xml_traverse_pc(root)
        df = pd.DataFrame(pc_dic.values(), columns=['path', 'tag', 'file_name', 'prod_name', 'ct'])
        with pd.ExcelWriter(f'{loc}/{ct}/excel/{ct}_rule.xlsx', engine='openpyxl', mode='a',
                            if_sheet_exists='replace') as writer:
            df.to_excel(writer, sheet_name='pc_master', index=False)
        pc_dic = {}

    return True
