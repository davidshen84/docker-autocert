FROM python:3.6
LABEL maintainer "Xi Shen <davidshen84@gmail.com>"

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt --upgrade
COPY main.py .

EXPOSE 8888
ENTRYPOINT ["python", "main.py"]
