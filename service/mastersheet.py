import pandas as pd


def master_sheet(loc, ct, fn, sn):
    df = pd.read_excel(f'{loc}/{ct}/excel/{fn}.xlsx', sheet_name=sn)
    df.sort_values(by=['Has Content'], ascending=False, inplace=True)
    df.drop_duplicates(subset=['Tags'], inplace=True)
    df = df[['Tags', 'Has Content']]
    with pd.ExcelWriter(f'{loc}/{ct}/excel/{ct}_rule.xlsx', engine='openpyxl', mode='a',
                        if_sheet_exists='replace') as writer:
        df.to_excel(writer, sheet_name='tag_master', index=False, columns=['tag', 'has_text'])
    return True


