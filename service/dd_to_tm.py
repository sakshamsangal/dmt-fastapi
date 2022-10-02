import pandas as pd


def fill_tm_by_dd(loc, ct):
    df_foo = pd.read_excel(f'{loc}/{ct}/excel/{ct}_rule.xlsx', sheet_name='data_dic')
    df_foo.set_index("map_tag", drop=True, inplace=True)
    dictionary = df_foo.to_dict(orient="index")
    my_ls = []
    for key, val in dictionary.items():
        ls = val['tag'].split(',')
        for item in ls:
            my_ls.append((key, item.strip()))
    df = pd.DataFrame(my_ls, columns=['tag', 'map_tag'])
    with pd.ExcelWriter(f'{loc}/{ct}/excel/{ct}_rule.xlsx', engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        df.to_excel(writer, sheet_name='tag_master', index=False)
    return True
