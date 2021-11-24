import pytest
import requests

from fastapi.testclient import TestClient

from fastapi.responses import FileResponse

from .main import app


client = TestClient(app)


# Routes


# /upload
def test_success_upload():

    url = 'http://127.0.0.1:8000/upload'
    files = {'file': open('./imgs/dog_01.bmp', 'rb')}
    response = requests.post(url, files=files)

    # assert response.status_code == 200
    assert response.status_code == 200

# /get-image/{filename}

# /write-message-on-image

# /decode-message-from-image/
