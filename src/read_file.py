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
    reg_exp = re.compile(b'Set Description:.*\n')
    # identify where it is
    try:
        return reg_exp.search(content).group().replace(
            b'Set Description:', b''
        ).replace(b'\n', b'').strip()  # remove all redundant characters
    except AttributeError:
        return None


# testing functions
if __name__ == '__main__':

    # define testing function for read_file() method
    assert read_file('./read_file.py')[0:2] == b'#!'

    # extract name for index
    CONTENT = read_file('../data/power_ssj2008-20071128-00001.txt')
    assert extract_name(CONTENT) == b'PRIMERGY RX300 S3 (Intel Xeon L5335)'

    print('All functions in', os.path.basename(__file__), 'are ok')
