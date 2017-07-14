#!/usr/bin/python
"""
    This file contains methods to pass the data from multiple files to
    a pandas DataFrame

    Author: Howard Cheung
    Date of creation: 2017/03/29
"""

# import python internal modules
import os

# import python third party modules
import pandas as pd

# import user-defined modules
import read_file

# define global variables


# define methods
def create_df(datadir: str, ext: str='txt') -> pd.DataFrame:
    """
        This method reads all files with the given file extension and
        reads them as if they are SPEC2008 data. Then, the data are
        passed to a pandas DataFrame with the following columns
            Name: name of the server
            Year: year of publication
            FormFac: form factor of the servers
            MaxPower: maximum power of the server in W
            IdlePower: idle power of the server in W

        Inputs:
        ==========
        datadir: string
            path to the data files

        ext: string
            file extension of the data files. Default 'txt'
    """

    datalist = []
    for name in os.listdir(datadir):
        filename = '/'.join([datadir, name])
        if os.path.isfile(filename) and ext in name[-len(ext):]:
            row_data = []
            content = read_file.read_file(filename)
            row_data.append(read_file.extract_name(content))
            row_data.append(read_file.extract_year(content))
            row_data.append(read_file.extract_form_factor(content))
            row_data.append(read_file.extract_max_power(content))
            row_data.append(read_file.extract_min_power(content))
            row_data.append(read_file.extract_cpu_speed(content))
            row_data.append(read_file.extract_core_num(content))
            for ind in range(10, 100, 10):
                row_data.append(read_file.extract_int_power(content, ind))
            datalist.append(row_data)

    return pd.DataFrame(data=datalist, columns=[
        'Name', 'Year', 'FormFac', 'MaxPower', 'IdlePower', 'CPU speed',
        'NumCores'
    ]+[''.join([str(ind), '%Power']) for ind in range(10, 100, 10)])

# testing functions
if __name__ == '__main__':

    # testing the main functions
    DATA_DIR = '../data/'
    NUM_FILES = len([
        name
        for name in os.listdir(DATA_DIR)
        if os.path.isfile('/'.join([DATA_DIR, name]))
    ])
    FINAL_DF = create_df('../data/', ext='txt')
    print(FINAL_DF)
    assert FINAL_DF.shape == (NUM_FILES, 7)
    assert set(FINAL_DF['Year']) == {
        2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016
    }

    print('All functions in', os.path.basename(__file__), 'are ok')
