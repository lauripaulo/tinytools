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
# 2021 - Corona virus code boredom challange :-)
#

import os
import json
import re
from PyPDF2 import PdfFileReader
from PyPDF2.utils import PdfReadError
from PyPDF2.pdf import PageObject
from pathlib import Path
from progress.bar import Bar
from progress.spinner import Spinner

PDF_MIN_SIZE = 512 # 512Kb

def getFilesFromFolder(folder, types=[".pdf"]):
    fileList = []
    if os.path.isdir(folder):
        for root, _, files in os.walk(folder):
            if len(files) == 0:
                break
            for file in files:
                path = os.path.join(root, file)
                size = os.path.getsize(path)
                extension = os.path.splitext(file)[-1]
                if extension == ".pdf":
                    info, pages = extract_information(path)
                    fileList.append({"filename": file, "fullpath": path, "size": size, "pages": pages, "info": info})
    return fileList


def findAllFolders(folder):
    folders = []
    folders.append(folder)
    if os.path.isdir(folder):
        for root, dirs, _ in os.walk(folder):
            for folder in dirs:
                fullpath = os.path.join(root, folder)
                folders.append(fullpath)
                #print('-> added %s folder.' % fullpath)
    return folders

def extract_information(pdf_path):
    information = None
    number_of_pages = 0
    try:
        with open(pdf_path, 'rb') as f:
            pdf = PdfFileReader(f, strict=False)
            if pdf.isEncrypted:
                pdf.decrypt('')
            docinfo = pdf.getDocumentInfo()
            number_of_pages = pdf.getNumPages()
            text = get_firstpage_text(pdf)
            if docinfo:
                information = {"author": docinfo.author, 
                    "creator": docinfo.creator,
                    "producer": docinfo.producer,
                    "subject": docinfo.subject,
                    "title": docinfo.title,
                    "text": text}
            else:
                information = {"error": "no info"}
    except Exception as error:
        information = {"error": error.args[0]}
    return information, number_of_pages

def get_firstpage_text(pdf):
    page = pdf.getPage(pageNumber=0)
    text = page.extractText()
    #text = re.sub(r'\W+', '', text)
    text = ''.join(c for c in text if c.isalnum() or c == ' ')
    return text

def find_pdf_books(folder):
    fileList = []
    print("PDF organizer\n")
    folders = findAllFolders(folder)
    with Bar('-> Analysing files ', max=len(folders)) as bar:
        for folder in folders:
            bar.next()
            folderFileList = getFilesFromFolder(folder)
            if len(folderFileList) > 0:
                fileList = fileList + folderFileList
    with open('data.json', 'w') as f:
        json.dump(fileList, f, ensure_ascii=False, indent=4)
        print("JSON saved.")
    print('\nFound %d files.' % len(fileList))


if __name__=="__main__":
    #find_pdf_books("/mnt/win10ssd/Users/lauri/Google Drive/Pessoal/RPG/")
    find_pdf_books("/mnt/win10ssd/Users/lauri/Google Drive/Pessoal/")