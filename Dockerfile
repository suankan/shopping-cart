FROM python:alpine

RUN pip3 install pyyaml

COPY ./code /code

WORKDIR /code
