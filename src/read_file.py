#!/usr/bin/python
"""
    This file contains scripts that helps to extract data from a file of
    SPEC 2008 data
"""

# import python internal modules
import os
import re

# import python third party modules


# import user-defined modules


# define global variables


# define methods
def read_file(filename: str) -> bytes:
    """
        This method reads the file specified by the user-given path. Return
        everything in the file in a bytes object.

        Inputs:
        ==========
        filename: string
            path to the file
    """

    with open(filename, 'rb') as openedfile:
        return openedfile.read()


def extract_name(content: bytes) -> bytes:
    """
        This function extracts the name of the server being tested and return
        a byte object. If it cannot find it, return a None object.

        Inputs:
        ==========
        content: bytes
            byte character obtained by reading a file
    """

    # define regular expression to be looked at
    reg_exp = re.compile(b'Set Description:.*Identical Nodes:', re.DOTALL)
    # identify where it is
    try:
        # remove all redundant characters
        return b' '.join(reg_exp.search(content).group().replace(
            b'Set Description:', b''
        ).replace(b'\n', b'').replace(b'# of Identical Nodes:', b'').split())
    except AttributeError:
        return None


def extract_year(content: bytes) -> int:
    """
        This function extracts the year of the server being tested and return
        an int object. If it cannot find it, return a None object.

        Inputs:
        ==========
        content: bytes
            byte character obtained by reading a file
    """

    # define regular expression to be looked at
    reg_exp = re.compile(b'Publication:.*\n')
    reg_exp2 = re.compile(b'Publication:.*,')
    # identify where it is
    try:
        statement = reg_exp.search(content).group()
        return int(statement.replace(
            reg_exp2.search(statement).group(), b''
        ).replace(b'\n', b'').strip())  # remove all redundant characters
    except AttributeError:
        return None


def extract_form_factor(content: bytes) -> int:
    """
        This function extracts the form factor of the server being tested and
        return an int object. If it cannot find it, return a float('nan')

        Inputs:
        ==========
        content: bytes
            byte character obtained by reading a file
    """

    # define regular expression to be looked at
    reg_exp = re.compile(b'Form Factor:.*\n')
    # identify where it is
    try:
        statement = reg_exp.search(content).group()
        return int(statement.replace(
            b'Form Factor:', b''
        ).replace(b'U', b'').strip())  # remove all redundant characters
    except AttributeError:
        return float('nan')


def extract_max_power(content: bytes) -> float:
    """
        This function extracts the maximum power consumption of the server
        during the test and return it as a float object. If it cannot find
        the power value, it returns a float('nan')

        Inputs:
        ==========
        content: bytes
            byte character obtained by reading a file
    """

    # define regular expression to be looked at
    reg_exp = reg_exp = re.compile(b'100\%.*\|')
    # identify where it is
    try:
        statement = reg_exp.search(content).group()
        return float(statement[-10:-2])  # remove all redundant characters
    except AtrributeError:
        return float('nan')
    except ValueError:
        return float('nan')


# testing functions
if __name__ == '__main__':

    # define testing function for read_file() method
    assert read_file('./read_file.py')[0:2] == b'#!'

    # extract name for index
    CONTENT = read_file('../data/power_ssj2008-20080612-00063.txt')
    assert extract_name(CONTENT) == \
        b'ProLiant DL120 G5 (2.83 GHz, Intel Xeon processor X3360)'

    # extract year
    assert extract_year(CONTENT) == 2008

    # extract form factor
    CONTENT2 = read_file('../data/power_ssj2008-20090811-00180.txt')
    assert extract_form_factor(CONTENT2) == 1

    # extract maximum power
    assert extract_max_power(CONTENT) == 136.0
    assert extract_max_power(CONTENT2) == 178.0

    print('All functions in', os.path.basename(__file__), 'are ok')
