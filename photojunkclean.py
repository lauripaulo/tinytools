#!/usr/bin/python3

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

from pathlib import Path
from exif import Image

IMAGE_MAX_SIZE = 512 # 512Kb
FILE_NAME_KEYWORDS = {"screenshot"}

@click.command()
@click.argument('folder')
@click.option('--size', default=IMAGE_MAX_SIZE, 
    help='max file size to be consider junk in kbytes (default={}Kb)'.format(IMAGE_MAX_SIZE))
@click.option('--move', default=None, help='folder to move junk')
def findjunk(folder, size, move):
    """ FOLDER: folder to search for junk images """
    click.echo("\nPhoto Junk Clean tool\n")
    size += size * 1024
    if (move and not os.path.isdir(move)) or move == folder:
        click.echo("Invalid move folder! Please, check the path. Aborting.")
        return
    else:
        click.echo("Folder to move files: %s" % move)
    if os.path.isdir(folder):
        fileList = []
        folders = findAllFolders(folder)
        for folder in folders:
            folderFileList = getFilesFromFolder(folder, size)
            if len(folderFileList) > 0:
                fileList = fileList + folderFileList
        click.echo('\nFound %d files.' % len(fileList))
    else:
        click.echo('Folder %s does not exists.' % folder)

def getFilesFromFolder(folder, maxsize, types=[".jpg", ".jpeg", ".png"]):
    click.echo('Inspecting folder: %s' % folder)
    fileList = []
    if os.path.isdir(folder):
        for root, _, files in os.walk(folder):
            for file in files:
                path = os.path.join(root, file)
                size = os.path.getsize(path)
                extension = os.path.splitext(file)[-1]
                if size <= maxsize and extension in types and not fromCamera(path):
                    fileList.append({"path": path, "size": size})
                    click.echo('--> found file %s (%d Kb)' % (path, int(size / 1024)))
    return fileList

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

def haveKeywords(fileName):
    for keyword in FILE_NAME_KEYWORDS:
        if keyword in fileName.lower():
            return True
    return False

def fromCamera(file):
    hasExif = False
    with open(file, 'rb') as image_file:
        analyseimg = Image(image_file)
        #click.echo(dir(analyseimg))
        hasExif = analyseimg.has_exif
    return hasExif

if __name__=="__main__":
    findjunk()