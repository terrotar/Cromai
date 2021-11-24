
import pytest

from fastapi.testclient import TestClient

from .main import app


client = TestClient(app)


# Routes


# /upload


# Success upload
def test_success_upload():
    url = 'http://127.0.0.1:8000/upload'
    files = {'file': open('./imgs/dog_01.bmp', 'rb')}
    response = client.post(url, files=files)

    assert response.status_code == 200


# Extension not allowed
def test_extension_not_allowed():
    url = 'http://127.0.0.1:8000/upload'
    files = {'file': open('./imgs/cat_not_bitmap.jpg', 'rb')}
    response = client.post(url, files=files)

    assert response.status_code == 422


# /get-image/{filename}


# Success get image
def test_success_get_image():
    url = 'http://127.0.0.1:8000/upload'
    files = {'file': open('./imgs/cat_02.bmp', 'rb')}
    response = client.post(url, files=files)

    url = 'http://127.0.0.1:8000/get-image?filename=cat_02'
    response = client.get(url)

    assert response.status_code == 200


# Image not found
def test_image_not_found():
    url = 'http://127.0.0.1:8000/get-image/?filename=cat_03'
    response = client.get(url)

    assert response.status_code == 400


# /write-message-on-image


# Success encode message
def test_success_encode_message():
    url = 'http://127.0.0.1:8000/upload'
    files = {'file': open('./imgs/cat_03.bmp', 'rb')}
    response = client.post(url, files=files)

    url = 'http://127.0.0.1:8000/write-message-on-image'
    data = {'filename': 'cat_03',
            'message': 'Test successful encoding message'}
    response = client.post(url, json=data)

    assert response.text == '{"new_file":"new_cat_03"}'


# Wrong encode message
def test_wrong_encode_message():
    url = 'http://127.0.0.1:8000/write-message-on-image'
    data = {'filename': 'cat_not_bitmap',
            'message': 'Test successful encoding message'}
    response = client.post(url, json=data)

    assert response.status_code == 400


# /decode-message-from-image/


# Sucess decode image's message
def test_success_decode_message():
    url = 'http://127.0.0.1:8000/decode-message-from-image?filename=new_cat_03'
    response = client.get(url)

    assert response.status_code == 200


# Wrong decode image's message
def test_wrong_decode_message():
    url = 'http://127.0.0.1:8000/decode-message-from-image?filename=cat_not_bitmap'
    response = client.get(url)

    assert response.status_code == 400
