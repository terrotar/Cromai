
from fastapi import File

from .settings import PATH, ALLOWED_EXTENSIONS

import imghdr

import shutil

import cv2

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

    # Check if file's in temporary folder
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


# Converts a message into a generator which returns
# 1 bit of the message each time.
def to_bit_generator(message: str):

    # Get byte's decimal
    for c in (message):
        o = ord(c)

        # Generate bits
        for i in range(8):
            yield (o & (1 << i)) >> i


# Encode a message in image
def encode_message(filepath: str, msg: str):

    # Set a dot(.) in the final of message
    set_dot = list(msg)
    if(set_dot[-1] != "."):
        msg = msg + "."

    # Create a generator for the hidden message
    hidden_message = to_bit_generator(msg)

    # Read the original image
    img = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
    for h in range(len(img)):
        for w in range(len(img[0])-1):
            # Write the hidden message into the least significant bit
            try:
                img[h][w] = (img[h][w] & ~1) | next(hidden_message)
            except Exception:
                pass
    # Write out the image with hidden message
    filepath = filepath.split(".")
    filepath = filepath[0].split("/")

    # Save new_img in temporary folder
    new_img_path = f"{PATH}/new_{filepath[-1]}.bmp"
    cv2.imwrite(new_img_path, img)

    return f"new_{filepath[-1]}"


# Decode image's message
def decode_message(filepath: str):

    # Open image with message encoded
    img = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
    i = 0
    bits = ''
    chars = []
    for row in img:
        for pixel in row:
            bits = str(pixel & 0x01) + bits
            i += 1
            if(i == 8):
                chars.append(chr(int(bits, 2)))
                i = 0
                bits = ''

    # Generate a list with message's chars in utf-8
    secret_message = []
    for char in chars:
        char = char.encode('utf-8')
        if(len(secret_message) < 1):
            secret_message.append(char)
        else:
            if(secret_message[-1] != "."):
                if(char.isascii() is True):
                    secret_message.append(char)
                else:
                    secret_message.append(".")
                    break
            else:
                break

    # Format encoded message
    message = ''
    for letter in secret_message:
        message += str(letter)
    test = ''
    message = message.split("'b'")
    for letter in message:
        test += letter

    return test[2:-2]
