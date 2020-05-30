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

IMAGE_MAX_SIZE = 2048 # 512Kb

@click.command()
@click.argument('folder')
@click.option('--size', default=IMAGE_MAX_SIZE, help='max file size to be consider junk in kbytes')
@click.option('--move', default=None, help='folder to move junk')
def findjunk(folder, size, move):
    """ FOLDER: folder to search for junk images """
    size += size * 1024
    if os.path.isdir(folder):
        fileList = []
        folders = findAllFolders(folder)
        for folder in folders:
            folderFileList = getFilesFromFolder(folder, size)
            if len(folderFileList) > 0:
                fileList.append(fileList)
        print('\nFound %d files.' % len(fileList))
    else:
        print('Folder %s does not exists.' % folder)

def getFilesFromFolder(folder, maxsize, types=[".jpg", ".jpeg", ".png"]):
    print('Inspecting folder: %s' % folder)
    fileList = []
    if os.path.isdir(folder):
        for root, _, files in os.walk(folder):
            for file in files:
                path = os.path.join(root, file)
                size = os.path.getsize(path)
                extension = os.path.splitext(file)[-1]
                if size <= maxsize and extension in types:
                    fileList.append({"path": path, "size": size})
                    print('--> found file %s (%d Kb)' % (path, int(size / 1024)))
    return fileList

def findAllFolders(folder):
    folders = []
    if os.path.isdir(folder):
        for root, dirs, files in os.walk(folder):
            for folder in dirs:
                fullpath = os.path.join(root, folder)
                folders.append(fullpath)
                #print('-> added %s folder.' % fullpath)
    return folders

if __name__=="__main__":
    findjunk()