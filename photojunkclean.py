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
import shutil

from pathlib import Path
from exif import Image
from progress.bar import Bar
from progress.spinner import Spinner

IMAGE_MAX_SIZE = 512 # 512Kb
FILE_NAME_KEYWORDS = {"screenshot"}

@click.command()
@click.argument('folder')
@click.option('--size', default=IMAGE_MAX_SIZE, 
    help='max file size to be consider junk in kbytes (default={}Kb)'.format(IMAGE_MAX_SIZE))
@click.option('--move', default=None, help='folder to move junk')
def findjunk(folder, size, move):
    """ FOLDER: folder to search for junk images """
    move = move.strip()
    folder = folder.strip()
    click.echo("\nPhoto Junk Clean tool\n")
    size += size * 1024
    if (move and not os.path.isdir(move)) or move == folder:
        click.echo("Invalid move folder: {}".format(move))
        click.echo("Please, check the path. Aborting.")
        return
    else:
        click.echo("Folder to move files: %s" % move)
    if os.path.isdir(folder):
        fileList = []
        click.echo("Analysing files...")
        folders = findAllFolders(folder)
        for folder in folders:
            folderFileList = getFilesFromFolder(folder, size)
            if len(folderFileList) > 0:
                fileList = fileList + folderFileList
        click.echo('\nFound %d files.' % len(fileList))
        if move and len(fileList) > 0:
            moveFiles(fileList, move)
            click.echo("Done moving junk images. Check it!")
        else:
            for file in fileList:
                click.echo('Junk file: {} ({} Kb)'.format(file["path"], int(file["size"] / 1024)))
    else:
        click.echo('Folder %s does not exists.' % folder)

def getFilesFromFolder(folder, maxsize, types=[".jpg", ".jpeg", ".png"]):
    fileList = []
    if os.path.isdir(folder):
        for root, _, files in os.walk(folder):
            if len(files) == 0:
                break
            with Bar('-> {} '.format(folder), max=len(files)) as bar:
                for file in files:
                    bar.next()
                    path = os.path.join(root, file)
                    size = os.path.getsize(path)
                    extension = os.path.splitext(file)[-1]
                    if size <= maxsize and extension in types:
                        if extension == ".png" or not fromCamera(path):
                            fileList.append({"path": path, "size": size})
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

def haveKeywords(fileName):
    for keyword in FILE_NAME_KEYWORDS:
        if keyword in fileName.lower():
            return True
    return False

def fromCamera(file):
    hasExif = False
    with open(file, 'rb') as image_file:
        try:
            analyseimg = Image(image_file)
            #click.echo(dir(analyseimg))
            hasExif = analyseimg.has_exif
        except:
            click.echo('\nError reading file: {}'.format(file))
    return hasExif

if __name__=="__main__":
    findjunk()