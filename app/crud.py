
from fastapi import File

from .settings import PATH, ALLOWED_EXTENSIONS

from PIL import BmpImagePlugin

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


# Create new_img with message
# Get file's bytes
def encode_message(filepath: str, message: str):
    file_bytes = []
    img = open(filepath, "rb")
    for i in list(bytes(img.read())):
        # i = format(i, '08b')
        file_bytes.append(i)

    # Set a dot(.) in the final of message
    set_dot = list(message.message)
    if(set_dot[-1] != "."):
        message.message = message.message + "."

    # Get message's bytes
    message_bytes = []
    for i in list(bytes(message.message, 'ascii')):
        i = format(i, '08b')
        message_bytes.append(i)

    # Split message in bits
    message_bits = []
    for byte in message_bytes:
        byte = list(byte)
        for i in byte:
            message_bits.append(i)

    # Encode the message's bits with file_bytes
    new_img = []
    pos = 0
    for img_byte in file_bytes:
        # Copy some initial bytes
        # Keeps the same header and also set
        # an index to decode after
        if(img_byte in file_bytes[0:10]):
            new_img.append(img_byte)
        else:
            if(pos < len(message_bits)):

                # Discard the LSB of first fyle byte
                img_byte = img_byte >> 1

                # Add message bit
                message_bit = int(message_bits[pos])
                img_byte = img_byte << 1 | message_bit
                new_img.append(img_byte)
                pos += 1
            else:
                # Copy the rest of file bytes
                new_img.append(img_byte)
                pos += 1

    # Set new_img to image and saves it in temporary folder
    # with prefix = "new_"
    input_image = BmpImagePlugin.BmpImageFile(filepath)
    output_image = input_image.copy()
    output_image.frombytes(bytes(new_img))

    # file is a pathlike
    filepath = filepath.split(".")
    filepath = filepath[0].split("/")

    # Save new_img in temporary folder
    new_img_path = f"{PATH}/new_{filepath[-1]}.bmp"
    output_image.save(f"{new_img_path}")

    return f"new_{filepath[-1]}"
