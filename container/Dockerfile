FROM python:3.10.5-alpine

WORKDIR /app

COPY . /app 

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "test.py"]
