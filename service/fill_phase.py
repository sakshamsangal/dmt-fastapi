import pandas as pd

from dao import read as rd


def fill_phase(loc, ct, alpha_no):
    ls = rd.get_phase(loc, ct, alpha_no)
    df = pd.read_excel(f'{loc}/{ct}/excel/dm_sheet/{ct}_dm.xlsx', sheet_name='Sheet1')
    df_new = pd.DataFrame(columns=df.columns)

    for tu in ls:
        for index, row in df.iterrows():
            if tu[0] == row[tu[3]]:
                if pd.isnull(df.iloc[index, 5]):
                    df.iat[index, 5] = tu[alpha_no]  # phase

        rows = df.loc[pd.isnull(df['phase']) == False, :]
        df_new = pd.concat([df_new, pd.DataFrame.from_records(rows)])
        df.drop(rows.index, inplace=True)
        df.reset_index(drop=True, inplace=True)

    df_new.to_excel(f'{loc}/{ct}/excel/dm_sheet/{ct}_phase.xlsx', index=False)
    df.to_excel(f'{loc}/{ct}/excel/dm_sheet/{ct}_dm.xlsx', index=False)
    return ls
