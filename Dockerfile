FROM python:3.9

WORKDIR /websocket_server

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install python-dotenv

COPY ./code ./code

CMD ["python", "./code/main.py"]
