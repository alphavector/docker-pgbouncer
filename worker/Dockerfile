FROM python:3.11.4-slim-bullseye

WORKDIR /worker
COPY . .

RUN pip install --no-cache-dir -r requirements.txt
CMD tail -f /dev/null