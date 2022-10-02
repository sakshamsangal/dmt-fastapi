import os

import pandas as pd


def map_xpath_to_tag(loc, ct, file_name, sn):
    os.makedirs(f'{loc}/{ct}/excel/dm_sheet', exist_ok=True)
    df = pd.read_excel(f'{loc}/{ct}/excel/{file_name}.xlsx', sheet_name=sn)
    t = ('m_xpath', 'comp', 'style', 'feat', 'comment', 'phase')
    for i, x in enumerate(t):
        df.insert(i, x, '')
    df['m_xpath'] = df['Legacy Xpaths']
    df_foo = pd.read_excel(f'{loc}/{ct}/excel/{ct}_rule.xlsx', sheet_name='xpath_map')
    df_foo.set_index("xpath", drop=True, inplace=True)
    dictionary = df_foo.to_dict(orient="index")

    for key, val in dictionary.items():
        df['m_xpath'].replace(to_replace=r'' + key + '\\b', value=val['xpath_map'], regex=True, inplace=True)
    df.to_excel(f'{loc}/{ct}/excel/dm_sheet/{ct}_xpath.xlsx', index=False)
    return True
