import argparse
import os
import re

# List of illegal chars to run through to replace in the filesystem walk
chars = ['~', '*', '\\', ':', '<', '>', '|', '?', '"', ',', '(', ')', ' ']

def ReplaceChars(value):
    for c in chars:
        value = value.replace(c, '_')
    return value


def RenamePath(root, path):
    newFilePath = ReplaceChars(path)
    os.rename(os.path.join(root, path), os.path.join(root, newFilePath))


def WalkFileSystem(dirroot):
    # Main Walk Through File System
    for root, dirs, files in os.walk(dirroot, topdown=False):
        for name in dirs:
            searchObj = re.search(r'[%s]' % ''.join(chars), name)
            if searchObj:
                print 'DIRECTORY: ',name
                RenamePath(root, name)

        for name in files:
            searchObj = re.search(r'[%s]' % ''.join(chars), name)
            if searchObj:
                print 'FILES: ',name
                RenamePath(root, name)


if __name__ == "__main__":
    # Calls the WalkFileSystem Function
    WalkFileSystem('/home/mohitsharma44/assignments/python_core/')
