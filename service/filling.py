import re

import pandas as pd


def remove_processed_record(df, df_new):
    rows = df.loc[pd.isnull(df['comp']) == False, :]
    df_new = pd.concat([df_new, pd.DataFrame.from_records(rows)])
    df.drop(rows.index, inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df, df_new


def remove_processed_record1(df, df_new):
    rows = df.loc[(df['comp'] != df['Component']) | (df['style'] != df['Styling']), :]
    df_new = pd.concat([df_new, pd.DataFrame.from_records(rows)])
    df.drop(rows.index, inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df, df_new


def update_df(df, short_str, comp, style, feat):
    for index, row in df.iterrows():
        if row['m_xpath'].endswith(short_str):
            df.iat[index, 1] = comp  # comp
            df.iat[index, 2] = style  # style
            if pd.isnull(df.iloc[index, 3]):
                df.iat[index, 3] = feat  # feat
    return df


def my_ends_with(loc, df, df_new):
    df_foo = pd.read_excel(f'{loc}/fixed.xlsx', sheet_name='comp_style')
    df_foo.set_index("id", drop=True, inplace=True)
    dictionary = df_foo.to_dict(orient="index")

    # id comp=1 h1=2 h2=3 text=4 feat=5
    for key, val in dictionary.items():
        df = update_df(df, f'/text', val['comp'], val['text_style'], val['feat'])
        df, df_new = remove_processed_record(df, df_new)

    for key, val in dictionary.items():
        df = update_df(df, f'/{key}', val['comp'], val['text_style'], val['feat'])
        df = update_df(df, f'/{key}/h1', val['comp'], val['h1_style'], val['feat'])
        df = update_df(df, f'/{key}/h2', val['comp'], val['h2_style'], val['feat'])
        df, df_new = remove_processed_record(df, df_new)

    return df, df_new


def fill_exception(loc, ct, df, df_new):
    df_foo = pd.read_excel(f'{loc}/{ct}/excel/{ct}_rule.xlsx', sheet_name='exception')
    df_foo.fillna('', inplace=True)
    df_foo.set_index("xpath", drop=True, inplace=True)
    dictionary = df_foo.to_dict(orient="index")

    for key, val in dictionary.items():
        xpath = re.compile(key)
        for index, row in df.iterrows():
            if re.fullmatch(xpath, row['m_xpath']):
                df.iat[index, 1] = val['comp']  # comp
                df.iat[index, 2] = val['styling']  # styling
                if pd.isnull(df.iloc[index, 3]):
                    df.iat[index, 3] = val['feat']  # feat
                df.iat[index, 4] = val['comm']  # comm

        df, df_new = remove_processed_record(df, df_new)
    return df, df_new


def fill_comp_style(loc, ct):
    df = pd.read_excel(f'{loc}/{ct}/excel/dm_sheet/{ct}_feat.xlsx', sheet_name='Sheet1')
    df_new = pd.DataFrame(columns=df.columns)
    df, df_new = fill_exception(loc, ct, df, df_new)
    df, df_new = my_ends_with(loc, df, df_new)

    df_new.to_excel(f'{loc}/{ct}/excel/dm_sheet/{ct}_dm_filled.xlsx', index=False)
    df.to_excel(f'{loc}/{ct}/excel/dm_sheet/{ct}_feat.xlsx', index=False)
    c = df.shape[0]

    df_new1 = pd.DataFrame(columns=df.columns)
    df_new.fillna('', inplace=True)
    df, df_new = remove_processed_record1(df_new, df_new1)
    df_new.to_excel(f'{loc}/{ct}/excel/dm_sheet/{ct}_dm_false.xlsx', index=False)
    df_new.drop(df_new.columns[0:6], axis=1, inplace=True)
    df_new.to_excel(f'{loc}/{ct}/excel/{ct}_dm_false.xlsx', index=False)

    return {'xpath_left': c, 'false_count': df_new.shape[0]}


def fill_feat(loc, ct):
    df_foo = pd.read_excel(f'{loc}/fixed.xlsx', sheet_name='fill_feat')
    df_foo.set_index("xpath", drop=True, inplace=True)
    dictionary = df_foo.to_dict(orient="index")
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


def fill_tm_by_dd(loc, ct):
    df_foo1 = pd.read_excel(f'{loc}/{ct}/excel/{ct}_rule.xlsx', sheet_name='tag_map')
    df_foo1['id'] = df_foo1['tag']
    df_foo1.set_index("id", drop=True, inplace=True)
    dictionary1 = df_foo1.to_dict(orient="index")

    df_foo = pd.read_excel(f'{loc}/{ct}/excel/{ct}_rule.xlsx', sheet_name='data_dic')
    df_foo.fillna('', inplace=True)
    df_foo.set_index("map_tag", drop=True, inplace=True)
    dictionary = df_foo.to_dict(orient="index")
    for key, val in dictionary.items():
        if val['tag'] == '':
            continue
        ls = val['tag'].split(',')
        for item in ls:
            dictionary1[item.strip()]['map_tag'] = key

    df = pd.DataFrame(dictionary1.values(), columns=['tag', 'map_tag'])
    with pd.ExcelWriter(f'{loc}/{ct}/excel/{ct}_rule.xlsx', engine='openpyxl', mode='a',
                        if_sheet_exists='replace') as writer:
        df.to_excel(writer, sheet_name='tag_map', index=False)
    return True
