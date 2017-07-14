#!/usr/bin/python
"""
    This file contains scripts to analyze the data

    Author: Howard Cheung
    Date of creation: 2017/03/28
"""

# import python internal modules
import ntpath
import os
from pathlib import Path
import pdb

# import python third party modules
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from numpy import isfinite
import pandas as pd

# import user-defined modules


# define global variables


# define methods
def summary_yr(datadf_ori: pd.DataFrame) -> pd.DataFrame:
    """
        This function summarizes the raw dataframe to create a new frame that
        is grouped based on the year of the data.

        Inputs:
        ==========
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
    summary_df.loc['Overall', :] = [
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
        ==========
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
    summary_df.loc['Overall', :] = [
        summary_df['Count'].sum(), datadf['CPU speed'].mean(),
        datadf['IdlePowerPortion'].mean(), datadf['IdlePowerPortion'].std()
    ]

    return summary_df


def cal_residual(summary: pd.DataFrame, datadf: pd.DataFrame) -> pd.DataFrame:
    """
        Calculate the residual of the estimated relative idle power consumption
        in the original dataframe based on the estimated value in the new
        dataframe. Return the original dataframe with the new columns
        'ResidualRelIdleYear' and 'ResidualRelIdleOverall'.

        Inputs:
        ==========
        summary: pandas.DataFrame
            pandas DataFrame calcalated from analysis.summary_yr_av()

        datadf: pandas.DataFrame
            pandas DataFrame calculated from create_df.create_df()
    """

    datadf.loc[:, 'ResidualRelIdleYear'] = float('nan')
    datadf.loc[:, 'ResidualRelIdleOverall'] = float('nan')
    for ind in summary.index:
        if ind != 'Overall':
            datadf.loc[datadf['Year']==ind, 'ResidualRelIdleYear'] = \
                datadf.loc[datadf['Year']==ind, 'IdlePowerPortion'] - \
                summary.loc[ind, 'IdlePowerPortion']
        else:
            datadf.loc[:, 'ResidualRelIdleOverall'] = \
                datadf.loc[:, 'IdlePowerPortion'] - \
                summary.loc[ind, 'IdlePowerPortion']

    return datadf


def residual_boxplot(filename: str, datadf_ori: pd.DataFrame):
    """
        This file plots the residual plot of idle power portion estimation
        as a box plot and saves the plot according to a user-defined
        path.

        Inputs:
        ==========
        filename: string
            path to the file of the boxplot

        datadf_ori: pandas.DataFrame
            pandas DataFrame calculated from create_df.create_df() and
            processed by analysis.cal_residual()
    """

    # make directory if it is unavailable
    if not Path(ntpath.split(filename)[0]).exists():
        mkdir(usrpath)

    # use one plot as an example for now
    # initialize
    data = []
    xtags = []
    # select data
    # drop na values
    datadf = datadf_ori[isfinite(datadf_ori['ResidualRelIdleYear'])]
    max_value = -1.0
    min_value = 1.0
    for time in datadf['Year'].unique():
        xtags.append(time)
        data.append(datadf.loc[datadf['Year']==time, 'ResidualRelIdleYear'])
        max_value = max(max_value, data[-1].max()+0.05)
        min_value = min(min_value, data[-1].min()-0.05)
    xtags.append('Overall')
    data.append(datadf.loc[:, 'ResidualRelIdleOverall'])
    # create box plot
    plt.figure(1)
    ax = plt.subplot(111)
    plt.boxplot(data, labels=xtags, showfliers=True)
    # set axis label
    plt.xlabel('Server Performance Data Publication Year')
    plt.ylabel('Residuals of Prediction')
    # set minor grid line
    # minorLocator = MultipleLocator(
        # (0.025 if max_value < 2.0 else 100)
        # if max_value <= 2000.0 else 2.5*10**(
            # len(str(int(max_value)))-2
        # )
    # )
    # ax.yaxis.set_minor_locator(minorLocator)
    majorLocator = MultipleLocator(
        (0.05 if max_value < 2.0 else 200)
        if max_value <= 2000.0 else 5.0*10**(
            len(str(int(max_value)))-2
        )
    )
    ax.yaxis.set_major_locator(majorLocator)
    plt.grid(b=True, which='major', color='k', axis='y')
    # plt.grid(b=True, which='minor', color='k', axis='y')
    # rotate x-axis labels
    locs, labels = plt.xticks()
    plt.setp(labels, rotation=90)
    # create more space for x-axis labels
    plt.subplots_adjust(top=0.95, bottom=0.2)
    # set minimum for y-axis as zero
    ax.set_ylim([min_value, max_value])
    # save plots
    plt.savefig(filename, dpi=300, frameon=False)
    plt.clf()


# testing functions
if __name__ == '__main__':

    from create_df import create_df

    # testing the main functions
    DATA_DIR = '../data/'
    FINAL_DF = create_df(DATA_DIR, ext='txt')
    SUMMARY = summary_yr(FINAL_DF)
    SUMMARY2 = summary_yr_av(FINAL_DF)
    FINAL_DF = cal_residual(SUMMARY2, FINAL_DF)  # calculate the residuals
    print(FINAL_DF)
    print(SUMMARY)
    print(SUMMARY2)
    assert SUMMARY.loc[2009, 'MaxPowerDens'] > 0.0
    assert SUMMARY.loc['Overall', 'MaxPowerDens'] > 0.0
    assert SUMMARY2.loc['Overall', 'IdlePowerPortion'] > 0.0
    assert SUMMARY2.loc['Overall', 'IdlePowerPortion'] < 1.0

    # make a plot
    residual_boxplot('./residual_plot.png', FINAL_DF)
    assert os.path.isfile('./residual_plot.png')

    # pass it to a file
    SUMMARY.to_csv('./summary.csv', sep=';')
    SUMMARY2.to_csv('./summary2.csv', sep=';')

    print('All functions in', os.path.basename(__file__), 'are ok')
