'''
Utility functions for the app
'''
import os

def mkdir_if_not(path):
    '''Create a directory if it does not exist'''
    if not os.path.exists(path):
        os.makedirs(path)

