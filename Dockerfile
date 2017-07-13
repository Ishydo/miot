FROM python:3
ENV PYTHONUNBEFFERED 1

RUN apt-get update && apt-get install -y binutils libproj-dev gdal-bin

RUN mkdir /code
WORKDIR /code

ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/
