
from fastapi import FastAPI, File, UploadFile, HTTPException

from fastapi.responses import FileResponse, JSONResponse

from .schemas import Message

from . import crud


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

    raise HTTPException(
        status_code=400,
        detail=f"File {filename} not found")


# White message on an image
@app.post("/write-message-on-image", response_class=JSONResponse)
async def write_message(message: Message):

    # Try to get file
    file = crud.check_upload(message.filename)
    if(file):

        filepath = crud.encode_message(filepath=file, message=message)

        if(crud.check_upload(filepath) is False):
            raise HTTPException(
                status_code=400,
                detail={"Error": f"File {message.filename} not encoded"})

        return {"new_file": f"{filepath}"}
        # return FileResponse(new_img_path)

    raise HTTPException(
        status_code=400,
        detail=f"File {message.filename} not found")
