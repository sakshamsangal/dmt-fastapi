import glob
import os
import time

from lxml import etree


# def xml_helper(loc, ct, tag_selected, xml_file_path):
#     context = etree.iterparse(xml_file_path, events=('end',), recover=True)
#     prod_name = os.path.splitext(os.path.basename(xml_file_path))[0]
#     # directory = f'{loc}/{ct}/xml/cx_{ct}/{prod_name}'
#     directory = f'{loc}/{ct}/xml/xml_{ct}_chunk/{prod_name}'
#     os.makedirs(directory, exist_ok=True)
#     my_dict = tag_selected.copy()
#     for event, elem in context:
#         tn = etree.QName(elem).localname
#         if tn in my_dict.keys():
#             # att = elem.attrib.items()
#             # fn = f'{directory}/{prod_name}_{tn}_{att[0][1]}_{my_dict[tn]}.xml'
#
#             fn = f'{directory}/{tn}_{my_dict[tn]}.xml'
#             my_dict[tn] += 1
#             with open(fn, 'wb') as f:
#                 f.write(bytearray('<?xml version="1.0" encoding="utf-8" ?>\n', 'utf-8'))
#                 f.write(etree.tostring(elem))
#             return fn


def get_folder_name(loc, ct):
    ls = []
    # for prod_path in sorted(glob.glob(f"{loc}/{ct}/xml/ox_{ct}/*"), key=os.path.getsize):
    for prod_path in sorted(glob.glob(f"{loc}/{ct}/xml/xml_{ct}_orig/*"), key=os.path.getsize):
        ls.append(prod_path.rsplit('\\', 1)[1])
    return ls


async def process_xml_chunk(loc, ct, tag_selected, att_sel, all_dir, products):
    tag_selected_dict = {}
    tag_selected = tag_selected.split(',')
    att_sel = att_sel.split(',')
    for x,y in zip(tag_selected, att_sel):
        tag_selected_dict[x] = [1, y]
    if all_dir:
        products = get_folder_name(loc, ct)
    for prod_name in products:
        # path_of_xml = f"{loc}/{ct}/xml/ox_{ct}/{prod_name}/*.xml"
        path_of_xml = f"{loc}/{ct}/xml/xml_{ct}_orig/{prod_name}/*.xml"
        for xml_file in sorted(glob.glob(path_of_xml), key=os.path.getsize):
            # x = xml_helper(loc, ct, tag_selected_dict, xml_file)
            context = etree.iterparse(xml_file, events=('end',), recover=True)
            prod_name = os.path.splitext(os.path.basename(xml_file))[0]
            # directory = f'{loc}/{ct}/xml/cx_{ct}/{prod_name}'
            directory = f'{loc}/{ct}/xml/xml_{ct}_chunk/{prod_name}'
            os.makedirs(directory, exist_ok=True)
            my_dict = tag_selected_dict.copy()
            for event, elem in context:
                tn = etree.QName(elem).localname
                if tn in my_dict.keys():
                    if my_dict[tn][1] == '':
                        x = f'{prod_name}_{tn}_{my_dict[tn][0]}.xml'
                    else:
                        att = dict(elem.attrib)
                        x = f'{prod_name}_{tn}_{att[my_dict[tn][1]]}_{my_dict[tn][0]}.xml'

                    fn = f'{directory}/{x}'
                    my_dict[tn][0] += 1
                    with open(fn, 'wb') as f:
                        f.write(bytearray('<?xml version="1.0" encoding="utf-8" ?>\n', 'utf-8'))
                        f.write(etree.tostring(elem))
                    # print(fn)
                    time.sleep(0.05)
                    yield x
