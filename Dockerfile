FROM python:3.13

RUN apt-get update && apt-get install -y sqlite3

WORKDIR RAG-Bot

RUN pip install --upgrade pip

RUN  pip install flake8

RUN pip install numpy

RUN pip install chromadb

RUN pip install together

RUN pip install python-dotenv

RUN pip install pypdf

RUN pip install langchain


# RUN python3 -m pip install --upgrade twine

COPY . .