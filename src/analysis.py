#!/usr/bin/python
"""
    This file contains scripts to analyze the data

    Author: Howard Cheung
    Date of creation: 2017/03/28
"""

# import python internal modules
import os

# import python third party modules
import pandas as pd

# import user-defined modules


# define global variables


# define methods
def summary_yr(datadf: pd.DataFrame) -> pd.DataFrame:
    """
        This function summarizes the raw dataframe to create a new frame that
        is grouped based on the year of the data.

        Inputs:
        datadf: pandas.DataFrame
            pandas DataFrame calculated from create_df.create_df()
    """

    datadf.dropna(inplace=True)  # drop all na values
    grouped = datadf.groupby('Year')
    idle_power_series = grouped['IdlePower'].mean()
    max_power_series = grouped['MaxPower'].mean()
    summary_df = pd.concat([
        grouped['IdlePower'].mean(), grouped['MaxPower'].mean(),
        grouped['IdlePower'].count()
    ], axis=1)
    summary_df.loc['All', :] = [
        datadf['IdlePower'].mean(), datadf['MaxPower'].mean(),
        datadf['IdlePower'].count()
    ]
    return summary_df

# testing functions
if __name__ == '__main__':

    from create_df import create_df

    # testing the main functions
    DATA_DIR = '../data/'
    FINAL_DF = create_df(DATA_DIR, ext='txt')
    SUMMARY = summary_yr(FINAL_DF)
    print(SUMMARY)
    assert SUMMARY.loc[2009, 'MaxPower'] > 0.0
    assert SUMMARY.loc['All', 'MaxPower'] > 0.0

    print('All functions in', os.path.basename(__file__), 'are ok')
