import glob
import os

from lxml import etree


def xml_helper(loc, ct, tag_selected, xml_file_path):
    context = etree.iterparse(xml_file_path, events=('end',), recover=True)
    prod_name = os.path.splitext(os.path.basename(xml_file_path))[0]
    directory = f'{loc}/{ct}/xml/cx_{ct}/{prod_name}'
    os.makedirs(directory, exist_ok=True)
    my_dict = tag_selected.copy()
    for event, elem in context:
        tn = etree.QName(elem).localname
        if tn in my_dict.keys():
            fn = f'{directory}/{prod_name}_{tn}_{my_dict[tn]}.xml'
            my_dict[tn] += 1
            print(fn)
            with open(fn, 'wb') as f:
                f.write(bytearray('<?xml version="1.0" encoding="utf-8" ?>\n', 'utf-8'))
                f.write(etree.tostring(elem))


def get_folder_name(loc, ct):
    ls = []
    for prod_path in sorted(glob.glob(f"{loc}/{ct}/xml/ox_{ct}/*"), key=os.path.getsize):
        ls.append(prod_path.rsplit('\\', 1)[1])
    return ls


def process_xml_chunk(loc, ct, tag_selected, all_dir, products):
    if all_dir:
        products = get_folder_name(loc, ct)
    for prod_name in products:
        path_of_xml = f"{loc}/{ct}/xml/ox_{ct}/{prod_name}/*.xml"
        for xml_file in sorted(glob.glob(path_of_xml), key=os.path.getsize):
            xml_helper(loc, ct, tag_selected, xml_file)
