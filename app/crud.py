
from fastapi import File

from .settings import PATH, ALLOWED_EXTENSIONS

import imghdr

import shutil

import os


# CHECKS


# Check the extension of uploaded file
def check_extension(filename: str):
    file_path = f"{PATH}/{filename}"
    check_ext = imghdr.what(file_path)
    if(check_ext not in ALLOWED_EXTENSIONS):
        os.remove(file_path)
        return False
    return check_ext


# Check if file was uploaded correctly
def check_upload(filename: str):

    # Insert ".bmp" in filename if it hasn't already
    check_name = filename.split(".")
    if(check_name[-1] != "bmp"):
        filename = filename + ".bmp"

    file_path = f"{PATH}/{filename}"
    if(os.path.isfile(file_path) is True):
        return file_path
    return False


# CREATE


# Save a file in the temporary server folder
def save_file(file: File(...)):
    file_path = f"{PATH}/{file.filename}"
    with open(file.filename, 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)
        shutil.move(file.filename, file_path)
