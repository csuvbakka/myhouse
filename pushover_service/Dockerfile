FROM python:3.7-stretch

COPY ./requirements.txt /app/requirements.txt
WORKDIR /app

RUN pip3 install -r requirements.txt
COPY . /app

CMD ["python3", "service.py"]
