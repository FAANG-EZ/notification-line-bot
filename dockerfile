FROM python:3.10.2

ENV TZ="Asia/Taipei"

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .