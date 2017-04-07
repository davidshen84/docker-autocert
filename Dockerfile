FROM python:3.6
LABEL maintainer "Xi Shen <davidshen84@gmail.com>"

RUN pip install tornado
COPY main.py /app
WORKDIR /app
