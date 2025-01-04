FROM python:3.12.4-slim

COPY ./collect_requirements.txt ./

RUN pip install -r ./collect_requirements.txt

COPY ./ ./

RUN pip install -r ./database/requirements.txt
