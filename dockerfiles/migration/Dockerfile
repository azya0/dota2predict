FROM python:3.12.4-slim

COPY ./requirements.txt ./

RUN pip install -r ./requirements.txt

COPY . ./

CMD ["alembic", "upgrade", "head"]
