# import configparser
#
# config = configparser.RawConfigParser()
# config.read('config.ini')
# # <form(.|\n)*?>(.|\n)*?</form>
# # x = config['deskbook']['form']
# # for item in x:
# #     print(item.strip())


import lxml.etree as et

xml = """
<form>
    <form>asas</form>
    <section>a</section>
    <section>a</section>
    <section class="asas" a="asas">
        <form>
            <form>asas</form>
            <section>a</section>
            <section>a</section>
        </form>
    </section>
</form>
"""

tree = et.fromstring(xml)

for bad in tree.xpath("//section"):
    bad.getparent().remove(bad)

with open('out.txt', 'wb') as f:
    f.write(et.tostring(tree, pretty_print=True))

if __name__ == '__main__':
    chapter = '//catalog//book'
    x = chapter.rsplit('/', 1)[1]
    print(x)
