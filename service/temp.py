# text = ['loc', 'ct']
# password = []
#
#
# res = ''
# for name in text:
#     s = f'''
#     <tr>
#         <td>{name}</td>
#         <td><input type="text" /></td>
#     </tr>'''
#     res += s
#
# for name in password:
#     s = f'''
#     <tr>
#         <td>{name}</td>
#         <td><input type="password" /></td>
#     </tr>'''
#     res += s
# with open('out.txt', 'w') as f:
#     f.write(res)

# s = ''
# print(s.split(','))


# creating a variable and storing the text
# that we want to search
import re
import configparser

config = configparser.RawConfigParser()
config.read('config.ini')

x = config['deskbook'].items()
tag_map = {}
xpath_map = {}
with open('leg.xml') as file:
    data = file.read()
    for tu in x:
        future = tu[0]
        present_ls = tu[1].split(',')
        for present in present_ls:
            if "/" in present:
                xpath_map[present] = future
            else:
                tag_map[present] = future

        #     data = re.sub(rf'<{present}(.|\n)*?>', f'<{future}>', data)
        #     data = re.sub(rf'</{present}>', f'</{future}>', data)

print(xpath_map)
print(tag_map)
# with open(r'out.txt', 'w', encoding='utf-8') as file:
#     file.write(data)
