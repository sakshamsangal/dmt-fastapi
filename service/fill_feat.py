import re

import pandas as pd


def fill_feature(loc, ct):
    # ls = rd.get_patt_to_be_replaced(loc, ct)
    df_foo = pd.read_excel(f'{loc}/fixed.xlsx', sheet_name='fill_feat')
    df_foo.set_index("xpath", drop=True, inplace=True)
    dictionary = df_foo.to_dict(orient="index")
    # ls = rd.get_patt_to_be_replaced(loc, ct)
    df = pd.read_excel(f'{loc}/{ct}/excel/dm_sheet/{ct}_tag.xlsx', sheet_name='Sheet1')
    for key, val in dictionary.items():
        # my_patt = tu[0].replace('*', '(.*?)')
        xpath = re.compile(key)
        for index, row in df.iterrows():
            if re.fullmatch(xpath, row['m_xpath']):
                df.iat[index, 0] = xpath.sub('\\1', row['m_xpath'])
                if pd.isnull(df.iloc[index, 3]):
                    df.iat[index, 3] = val['feat']  # feat

    df.to_excel(f'{loc}/{ct}/excel/dm_sheet/{ct}_feat.xlsx', index=False)
    return True
