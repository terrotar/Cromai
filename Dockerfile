FROM python:3.9

WORKDIR /Cromai

COPY ./requirements.txt /Cromai/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /Cromai/requirements.txt

COPY ./app /Cromai/app

COPY ./Documents /Cromai/Documents

COPY ./README.md /Cromai/README.md

RUN apt-get update

RUN apt-get install ffmpeg libsm6 libxext6 -y

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]