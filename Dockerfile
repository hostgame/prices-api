FROM library/python:3.8-slim

COPY requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt
COPY src/ /app

CMD ["python", "app.py"]