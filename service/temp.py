from lxml import etree

res = ''
def xml_traverse(root, space):
    global res
    tag_name = etree.QName(root).localname
    if tag_name == 'name':
        res += space + root.text + '\n'
    for child in root:
        if type(child) == etree._Element:
            xml_traverse(child, space + '    ')


xml_file = 'food.xml'
parser = etree.XMLParser(recover=True)
tree = etree.parse(xml_file, parser)
root = tree.getroot()
xml_traverse(root, '')


with open('out.txt', 'w') as f:
    f.write(res)