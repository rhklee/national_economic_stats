import pandas as pd
import numpy as np
from collections import deque

def upsert_key(col, annual_change_dict):
    if not col in annual_change_dict:
        annual_change_dict[col] = []

def calc_annual_change(p, c):
    return 100 * (c-p)/p

def insert_annual_change(annual_change_dict, col, v):
    annual_change_dict[col].append(v)


if __name__ == "__main__":

    df = pd.read_csv('manuf.csv', 
        usecols=[x for x in range(72) if x not in {2,3,4,5,6}],
        nrows=8)

    # print(df)
    # print(df.columns)

    annual_change = {'Country': []}

    for ri in range(df.shape[0]):
        annual_change['Country'].append(df.iat[ri, 1])
        for ci in range(3, df.shape[1]):
            upsert_key(df.columns[ci], annual_change)

            if np.isnan(df.iat[ri, ci]):
                annual_change[df.columns[ci]].append(np.nan)
                continue
            if ci != 3 and np.isnan(df.iat[ri, ci-1]):
                annual_change[df.columns[ci]].append(np.nan)
                continue

            # Current value is nan and preceding value is not nan
            cv = calc_annual_change(df.iat[ri, ci-1], df.iat[ri, ci])
            insert_annual_change(annual_change, df.columns[ci], cv)

            # print("{}, {} : {}".format(ri, ci, df.iat[ri,ci]))

    # print(annual_change)

    df2 = pd.DataFrame(annual_change)
    
    # print(df2)
    # print(df2.groupby([ str(y) for y in range(1951, 1960) ]))

    df2.to_csv('output.csv')

