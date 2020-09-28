#!/usr/bin/python3

# MIT License

# Copyright (c) 2020 Lauri P. Laux Jr

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

#
# Find images with less than the designed size and move them to a 
# folder for inspection. The aim is to move all screenshots and
# junk images from social media from a folder of your own
# phone/camera "good" photos.
#
# Lauri P. Laux - lauripaulo@hotmail.com
# 2020 - Corona virus code boredom challange :-)

import os
import json
import argparse
import pathlib

from pathlib import Path
from progress.bar import Bar
from progress.spinner import Spinner

def findAllFolders(folder):
    folders = [f.path for f in os.scandir(folder) if f.is_dir()]
    print("\nFound {} folders.".format(len(folders)))
    return folders

def main(folder):
    foundFolderList = []
    folders = findAllFolders(folder)
    for folder in folders:
        subFolders = [f.path for f in os.scandir(folder) if f.is_dir()]
        if len(subFolders) == 0:
            foundFolderList.append(folder)
            print("Found folder: '{}'".format(folder))
    return foundFolderList

def find_folders_without_subfolders():
    folder = args.folder
    logFile = args.logfile
    print("\n{}".format(parser.description))
    print("Folder: '{}'".format(folder))
    print("Log file: '{}'".format(logFile))
    foundFolderList = main(folder)
    with open(os.path.join(pathlib.Path().absolute(), logFile), "w+") as log_file:
        json.dump(foundFolderList, log_file)
    pass

if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Folder Without SubFolders - v0.1")
    parser.add_argument("folder", metavar="folder", type=str, 
        help="folder to search.")
    parser.add_argument("logfile", metavar="logfile", type=str, 
        help="log file where the results are kept.")
    args = parser.parse_args()
    if not args.folder or not args.logfile:
        parser.print_help()
    else:
        find_folders_without_subfolders()