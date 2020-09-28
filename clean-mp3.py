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
#

import click
import os
import shutil

from pathlib import Path
from exif import Image
from progress.bar import Bar
from progress.spinner import Spinner


def findAllFolders(folder):
    folders = []
    folders.append(folder)
    if os.path.isdir(folder):
        for root, dirs, _ in os.walk(folder):
            for folder in dirs:
                fullpath = os.path.join(root, folder)
                folders.append(fullpath)
                #click.echo('-> added %s folder.' % fullpath)
    return folders

def moveFiles(fileList, toFolder):
    with Bar('Moving files', max=len(fileList)) as bar:
        for file in fileList:
            _, moveFileName = os.path.split(file["path"])
            newFile = os.path.join(toFolder, moveFileName)
            suffix = 0
            while os.path.isfile(newFile):
                _, name = os.path.split(newFile)
                name, ext = os.path.splitext(name)
                suffix += 1
                newFile = os.path.join(toFolder, "{}-({}){}".format(name, suffix, ext))
            shutil.move(file["path"], newFile)
            bar.next()

@click.command()
@click.argument('folder')
def find_duplicates(folder):
    folder = folder.strip()
    click.echo("\nMP3 duplicate finder tool\n")
    click.echo("Folder: {}".format(folder))
    pass

if __name__=="__main__":
    find_duplicates()
    SystemExit()