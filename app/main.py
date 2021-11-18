
from fastapi import FastAPI, File, UploadFile, HTTPException

from fastapi.responses import FileResponse


import tempfile

import shutil

import os


# Create temporary directory
temp = tempfile.TemporaryDirectory()
PATH = temp.name

# Allowed extensions for files
ALLOWED_EXTENSIONS = ['bmp']


# FastAPI instance
app = FastAPI()


# Upload a file
@app.post("/upload")
async def upload(file: UploadFile = File(...)):

    # Checks if the extension is allowed
    check_file = file.filename.split('.')
    if(check_file[-1] not in ALLOWED_EXTENSIONS):
        raise HTTPException(status_code=415, detail="File extension must be .bmp")

    try:
        # Saves the file and move it to PATH
        with open(file.filename, 'wb') as buffer:
            shutil.copyfileobj(file.file, buffer)
            shutil.move(file.filename, f"{PATH}/{file.filename}")

        # Checks if file was correctly saved
        if(os.path.isfile(f"{PATH}/{file.filename}") is True):
            return {"message": f"File {file.filename} saved in directory {PATH}"}

    except Exception:
        raise HTTPException(status_code=400, detail="File not saved")


# Get an image by its name
@app.get("/get-image/{filename}")
def get_image(filename: str):
    filename = filename + ".bmp"
    if(os.path.isfile(f"{PATH}/{filename}") is True):
        return FileResponse(f"{PATH}/{filename}")

    raise HTTPException(status_code=400, detail=f"File {filename} not found")
