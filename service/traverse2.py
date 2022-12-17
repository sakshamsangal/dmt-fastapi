import glob
import os
import re

from lxml import etree
from service import create_master as cm
import configparser

xpath_dic = {}
wrapper = set()
tag_map = {}
xpath_map = {}
file_name = ''
prod_name = ''


def xml_traverse_xpath(root, xpath):
    tag_name = etree.QName(root).localname
    if tag_name not in tag_map:
        tag_map[tag_name] = {}
        tag_map[tag_name]['tag'] = 'wrapper'
        tag_map[tag_name]['att'] = []
    # if tag_name == tag_map[tag_name]:
    root.attrib.clear()
    root.tag = tag_map[tag_name]['tag']
    x = tag_map[tag_name]['att']
    for item in x:
        root.attrib[item] = ''

    if xpath not in xpath_dic:
        xpath_dic[xpath] = (tag_name, xpath, file_name, prod_name)

    for child in root:
        if type(child) == etree._Element:
            xml_traverse_xpath(child, xpath + '/' + etree.QName(child).localname)


def sole_by_xpath(loc, content_type, all_dir, products):
    global xpath_dic, file_name, prod_name
    my_root = ''
    for root, f_name, p_name in cm.get_xml_root(loc, content_type, all_dir, products):
        file_name = f_name
        prod_name = p_name
        my_root = root
        for k, v in xpath_map.items():
            x = str(k).rsplit('/', 1)[1]
            print(x)
            y, *rem = v.split('@')
            tag_map[y] = {
                'tag': y,
                'att': rem
            }
            for p in root.xpath(k):
                p.tag = y

        xml_traverse_xpath(root, etree.QName(root).localname)
        for bad in root.xpath("//not-render"):
            bad.getparent().remove(bad)

    fstring = etree.tostring(my_root).decode()
    with open('out.xml', 'w') as f:
        fstring = re.sub(rf'<\?([^xml])(.|\n)*?\?>', f'', fstring)
        fstring = fstring.replace("<wrapper>", '')
        fstring = fstring.replace("</wrapper>", '')
        f.write(fstring)

    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse('out.xml', parser)
    tree.write('out.xml', pretty_print=True)
    return True


def my_temp(loc, ct, products):
    global xpath_map
    config = configparser.RawConfigParser()
    config.read('config.ini')
    x = config['deskbook'].items()

    for prod_name in products:
        path_of_xml = f"{loc}/{ct}/xml/xml_{ct}_orig/{prod_name}/*.xml"
        for xml_file in sorted(glob.glob(path_of_xml), key=os.path.getsize):
            print(xml_file)
            with open(xml_file) as file:
                # data = file.read()
                for tu in x:
                    future = tu[0]
                    present_ls = tu[1].split(',')
                    for present in present_ls:
                        if "/" in present:
                            xpath_map[present] = future
                        else:
                            y, *rem = future.split('@')
                            tag_map[present] = {
                                'tag': y,
                                'att': rem
                            }
        sort_data = sorted(xpath_map.items(), reverse=True)
        xpath_map = dict(sort_data)
        print(xpath_map)
        print(tag_map)


if __name__ == '__main__':
    loc = r'C:\Users\saksangal\Pictures\saksham'
    ct = 'deskbook'
    all_dir = False
    prod = ['ppct65']
    my_temp(loc, ct, prod)
    sole_by_xpath(loc, ct, all_dir, prod)
