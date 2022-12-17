from lxml import etree
from service import create_master as cm

import pandas as pd

xpath_dic = {}
file_name = ''
prod_name = ''


def xml_traverse_xpath(root, xpath):
    tag_name = etree.QName(root).localname
    if xpath not in xpath_dic:
        xpath_dic[xpath] = (tag_name, xpath, file_name, prod_name)

    for child in root:
        if type(child) == etree._Element:
            xml_traverse_xpath(child, xpath + '/' + etree.QName(child).localname)


def sole_by_xpath(loc, content_type, all_dir, products):
    global xpath_dic, file_name, prod_name
    ct = content_type

    for root, f_name, p_name in cm.get_xml_root(loc, content_type, all_dir, products):
        file_name = f_name
        prod_name = p_name
        xml_traverse_xpath(root, etree.QName(root).localname)
    print(xpath_dic)
    df = pd.DataFrame(xpath_dic.values(), columns=['tag', 'xpath', 'file_name', 'prod_name'])
    with pd.ExcelWriter(f'{loc}/{ct}/excel/{ct}_rule.xlsx', engine='openpyxl', mode='a',
                        if_sheet_exists='replace') as writer:
        df.to_excel(writer, sheet_name='xpath_master', index=False)

    return True


if __name__ == '__main__':
    loc = r'C:\Users\saksangal\Pictures\saksham'
    ct = 'deskbook'
    all_dir = False
    prod = ['ppct65']
    sole_by_xpath(loc, ct, all_dir, prod)
