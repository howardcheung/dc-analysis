#!/usr/bin/python
"""
    This file contains scripts to analyze the data

    Author: Howard Cheung
    Date of creation: 2017/03/28
"""

# import python internal modules
import os
import pdb

# import python third party modules
import pandas as pd

# import user-defined modules


# define global variables


# define methods
def summary_yr(datadf_ori: pd.DataFrame) -> pd.DataFrame:
    """
        This function summarizes the raw dataframe to create a new frame that
        is grouped based on the year of the data.

        Inputs:
        datadf_ori: pandas.DataFrame
            pandas DataFrame calculated from create_df.create_df()
    """

    datadf = datadf_ori.dropna()  # drop all na values

    # adjust the values
    datadf.loc[:, 'AdjIdlePower'] = datadf.loc[:, 'IdlePower'] /\
        datadf.loc[:, 'FormFac']
    datadf.loc[:, 'AdjMaxPower'] = datadf.loc[:, 'MaxPower'] /\
        datadf.loc[:, 'FormFac']
    datadf.loc[:, 'AdjNumCores'] = datadf.loc[:, 'NumCores'] /\
        datadf.loc[:, 'FormFac']

    # group the data
    grouped = datadf.groupby('Year')
    summary_df = pd.concat([
        grouped['AdjIdlePower'].mean(), grouped['AdjMaxPower'].mean(),
        grouped['IdlePower'].count(), grouped['CPU speed'].mean(),
        grouped['AdjNumCores'].mean()
    ], axis=1)
    summary_df.loc['All', :] = [
        datadf['AdjIdlePower'].mean(), datadf['AdjMaxPower'].mean(),
        datadf['IdlePower'].count(), datadf['CPU speed'].mean(),
        datadf['AdjNumCores'].mean()
    ]
    summary_df.columns = [
        'AdjIdlePower', 'AdjMaxPower', 'Count', 'AvCPUspd',
        'NumCoresPer1U'
    ]

    # calculate the required density values
    summary_df.loc[:, 'IdlePowerDens'] = \
        summary_df.loc[:, 'AdjIdlePower']*42.0/4.379*0.47
    summary_df.loc[:, 'MaxPowerDens'] = \
        summary_df.loc[:, 'AdjMaxPower']*42.0/4.379*0.47
    summary_df.loc[:, 'NumCoresPerRack'] = \
        summary_df.loc[:, 'NumCoresPer1U']*42.0*0.47

    return summary_df



def summary_yr_av(datadf: pd.DataFrame) -> pd.DataFrame:
    """
        This function summarizes the raw dataframe to create a new frame that
        is grouped based on the year of the data without filtering the NaN
        form factors.

        Inputs:
        datadf: pandas.DataFrame
            pandas DataFrame calculated from create_df.create_df()
    """

    # adjust the values
    datadf.loc[:, 'IdlePowerPortion'] = datadf.loc[:, 'IdlePower'] /\
        datadf.loc[:, 'MaxPower']

    # group the data
    grouped = datadf.groupby('Year')
    summary_df = pd.concat([
        grouped['IdlePowerPortion'].count(), grouped['CPU speed'].mean(),
        grouped['IdlePowerPortion'].mean(), grouped['IdlePowerPortion'].std()
    ], axis=1)
    summary_df.columns = [
        'Count', 'AvCPUspd', 'IdlePowerPortion', 'IdlePowerPortion.std'
    ]
    summary_df.loc['All', :] = [
        summary_df['Count'].sum(), datadf['CPU speed'].mean(),
        datadf['IdlePowerPortion'].mean(), datadf['IdlePowerPortion'].std()
    ]

    return summary_df

# testing functions
if __name__ == '__main__':

    from create_df import create_df

    # testing the main functions
    DATA_DIR = '../data/'
    FINAL_DF = create_df(DATA_DIR, ext='txt')
    SUMMARY = summary_yr(FINAL_DF)
    SUMMARY2 = summary_yr_av(FINAL_DF)
    print(SUMMARY)
    print(SUMMARY2)
    assert SUMMARY.loc[2009, 'MaxPowerDens'] > 0.0
    assert SUMMARY.loc['All', 'MaxPowerDens'] > 0.0
    assert SUMMARY2.loc['All', 'IdlePowerPortion'] > 0.0
    assert SUMMARY2.loc['All', 'IdlePowerPortion'] < 1.0

    # pass it to a file
    SUMMARY.to_csv('./summary.csv', sep=';')
    SUMMARY2.to_csv('./summary2.csv', sep=';')

    print('All functions in', os.path.basename(__file__), 'are ok')
