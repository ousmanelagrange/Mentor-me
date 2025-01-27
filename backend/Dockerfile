FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y gcc libffi-dev python3-dev && \
    apt-get clean 

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "mentor_me.wsgi:application"]
