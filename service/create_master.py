import glob
import os

from lxml import etree


def get_folder_name(loc, ct):
    ls = []
    for prod_path in sorted(glob.glob(f"{loc}/{ct}/xml/ox_{ct}/*"), key=os.path.getsize):
        ls.append(prod_path.rsplit('\\', 1)[1])
    return ls


def get_xml_root(loc, ct, all_dir, products):
    if all_dir:
        products = get_folder_name(loc, ct)
    for prod_name in products:
        path_of_xml = f"{loc}/{ct}/xml/xml_{ct}_orig/{prod_name}/*.xml"
        for xml_file in sorted(glob.glob(path_of_xml), key=os.path.getsize):
            print(path_of_xml)
            file_name = os.path.basename(xml_file)
            parser = etree.XMLParser(recover=True)
            tree = etree.parse(xml_file, parser)
            yield tree.getroot(), file_name, prod_name
