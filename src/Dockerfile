FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=app.py

EXPOSE 8080

#CMD ["python3", "app.py"]
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]