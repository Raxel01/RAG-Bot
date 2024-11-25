FROM python:3.10-bullseye

WORKDIR RAG-Bot

RUN pip install --upgrade pip

RUN  pip install flake8

RUN pip install numpy

RUN pip install chromadb

RUN pip install together


RUN pip install --upgrade build

# RUN python3 -m pip install --upgrade twine

COPY . .