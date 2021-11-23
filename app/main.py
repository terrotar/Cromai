
from fastapi import FastAPI, File, UploadFile, HTTPException

from fastapi.responses import FileResponse, JSONResponse

from PIL import BmpImagePlugin

from .schemas import Message

from . import crud, settings


# FastAPI instance
app = FastAPI()


# Upload a file
@app.post("/upload")
async def upload(file: UploadFile = File(...)):

    # Save the file and moves it to temporary folder
    crud.save_file(file)

    # Check if file's extension is allowed
    check_extension = crud.check_extension(file.filename)
    if(check_extension != "bmp"):
        raise HTTPException(status_code=400,
                            detail="Only extension .bmp is allowed")

    # Check if file was correctly saved
    check_upload = crud.check_upload(file.filename)
    if(check_upload is False):
        raise HTTPException(status_code=400,
                            detail="File not saved")

    return {"message": f"File {file.filename} was correctly uploaded"}


# Get an image by its name
@app.get("/get-image/{filename}")
def download_file(filename: str):

    # Try to get file
    file = crud.check_upload(filename)
    if(file):
        return FileResponse(file)

    raise HTTPException(status_code=400, detail=f"File {filename} not found")


# White message on an image
@app.post("/write-message-on-image", response_class=JSONResponse)
async def write_message(message: Message):

    # Try to get file
    file = crud.check_upload(message.filename)
    if(file):

        # Get file's bytes
        file_bytes = []
        img = open(file, "rb")
        for i in list(bytes(img.read())):
            # i = format(i, '08b')
            file_bytes.append(i)

        # Set a dot(.) in the final of message
        set_dot = list(message.message)
        if(set_dot[-1] != "."):
            message.message = message.message + "."

        # Open message in bytes
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

        # Get size of file_bytes equal size of message_bytes
        file_message_bytes = file_bytes[:len(message_bytes)*8]
        # Create the new binary with message in LSB
        new_img = []
        pos = 0
        for img_byte in file_bytes:
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
                    new_img.append(img_byte)
                    pos += 1

        # Set new_img to image and saves it in temporary folder
        # with prefix = "new_"
        input_image = BmpImagePlugin.BmpImageFile(file)
        output_image = input_image.copy()
        output_image.frombytes(bytes(new_img))
        file = file.split(".")
        file = file[0].split("/")
        new_img_path = f"{settings.PATH}/new_{file[-1]}.bmp"
        output_image.save(f"{new_img_path}")

        new_img_bytes = []
        for img_byte in new_img:
            img_byte = format(img_byte, '08b')
            new_img_bytes.append(img_byte)

        return {"new_file": f"new_{file[-1]}"}
        # return FileResponse(new_img_path)
        """
        return {
            # "file_bytes_qtd": f"{len(file_bytes)}",
            # "new_img_bytes": f"{new_img_bytes [0:8]}",
            "new_img": f"{bytearray(new_img[1:-2])}",
            # "file_LSB": f"{img_LSB}",
            # "First_least_significant_bit": f"{list(file_bytes[0])[-1]}",
            # "necessary_bytes_message": f"{len(message_bytes)*8}",
            # "file_message_bytes": f"{file_message_bytes}",
            # "message_bits": f"{message_bits}"}
           # "message_bytes": f"{message_bytes}"}
           """
    raise HTTPException(
        status_code=400, detail=f"File {message.filename} not found")
