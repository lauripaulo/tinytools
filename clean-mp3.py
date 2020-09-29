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
import json
import pathlib

from pathlib import Path
from progress.bar import Bar
from progress.spinner import Spinner
from mp3_tagger import MP3File, VERSION_1, VERSION_2, VERSION_BOTH

class Duplicates:

    def __init__(self):
        self.total = 0

    def onemore(self):
        self.total = self.total + 1

DUPLICATES = Duplicates()

def findAllFolders(folder):
    folders = []
    folders.append(folder)
    spinner = Spinner()
    if os.path.isdir(folder):
        for root, dirs, _ in os.walk(folder):
            for folder in dirs:
                fullpath = os.path.join(root, folder)
                folders.append(fullpath)
                spinner.message = "Analysing folders: "
                spinner.next()
    click.echo("\nFound {} folders.".format(len(folders)))
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

def getFilesFromFolder(folder, types=[".mp3"]):
    fileList = []
    missign_tracks = []
    tracks = []
    iterations = 0
    spinner = Spinner()
    if os.path.isdir(folder):
        for root, _, files in os.walk(folder):
            if len(files) == 0:
                break
            for file in files:
                iterations += 1
                spinner.message = "Analysing folder: '{}' - Files: {} - Duplicates: {} - ".format(folder, iterations, DUPLICATES.total)
                spinner.next()
                path = os.path.join(root, file)
                size = os.path.getsize(path)
                extension = os.path.splitext(file)[-1]
                if extension in types:
                    mp3 = MP3File(path)
                    tags = get_mp3_tags(mp3)
                    tracks.append(tags)
                    filter_duplicates(tags, extension, types, path, fileList, size)
            spinner.clearln()
            missign_tracks.append(find_missing_tracks(tracks))
    return fileList, missign_tracks

def get_mp3_tags(mp3):
    tags = "empty"
    try:
        tags = mp3.get_tags()
    except UnicodeDecodeError as err:
        click.echo("\nError retreiving tags, file: {} - error: {}".format(path, err.reason))
    except:
        click.echo("\nBad MP3 tags , file: {}".format(path))
    return tags

def find_missing_tracks(tracks):
    missing_tracks = []
    for track in tracks:
        track_number = track['ID3TagV2']['track']
        missing_tracks.append(track_number)
    return missing_tracks

def filter_duplicates(tags, extension, types, path, fileList, size):
    for i in range(9): 
        suffix  = "({})".format(i)
        suffix2 = "_{}.".format(i)
        if suffix in path or suffix2 in path:
            track = "empty"
            name = "empty"
            if tags['ID3TagV2'] and tags['ID3TagV2']['track']:
                track = tags['ID3TagV2']['track']
            if tags['ID3TagV2'] and tags['ID3TagV2']['song']:
                name = tags['ID3TagV2']['song']
            DUPLICATES.onemore()
            fileList.append({"path": path, "size": size, "track": track, "name": name})

@click.command()
@click.argument('folder')
def find_duplicates(folder):
    folder = folder.strip()
    click.echo("\nMP3 duplicate finder tool\n")
    click.echo("Folder: {}".format(folder))
    folders = findAllFolders(folder)
    fileList = []
    for folder in folders:
        folderFileList, missing_tracks = getFilesFromFolder(folder)
        click.echo("Missing tracks: {}".format(missing_tracks))
        if len(folderFileList) > 0:
            fileList = fileList + folderFileList
    if len(fileList) > 0:
        click.echo("Found {} duplicated files.".format(len(fileList)))
        with open(os.path.join(pathlib.Path().absolute(), "duplicated-files-log.json"), "w+") as log_file:
            json.dump(fileList, log_file)
        moveFiles(fileList, "D:\\Work\\MP3-Duplicada")
        click.echo("\nDone.\n")
    else:
        click.echo("\nNo duplicates found.\n")

if __name__=="__main__":
    find_duplicates()
    SystemExit()