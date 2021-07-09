FROM python:3.9-slim

WORKDIR /app
COPY ./src /app

RUN pip3 install --upgrade pip
RUN pip3 install uvicorn fastapi selenium bs4

CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--reload"]
