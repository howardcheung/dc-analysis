#!/usr/bin/python
"""
    This file contains scripts that helps to extract data from a file of
    SPEC 2008 data
"""

# import python internal modules
import os

# import python third party modules


# import user-defined modules


# define global variables


# define methods
def read_file(filename: str):
    """
        This method reads the file specified by the user-given path. Return
        everything in the file in a string.

        Inputs:
        ==========
        filename: string
            path to the file
    """

    with open(filename, 'rb') as openedfile:
        return openedfile.read()


# testing functions
if __name__ == '__main__':

    # define testing function for read_file() method
    assert read_file('./read_file.py')[0:2] == b'#!'

    print('All functions in', os.path.basename(__file__), 'are ok')
