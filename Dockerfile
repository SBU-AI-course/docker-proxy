FROM python:3.9-alpine

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 80
# CMD ["python3", "waitress_server.py"]
CMD ["flask", "--app", "main", "run", "--host=0.0.0.0", "--port=80", "--debug"]
