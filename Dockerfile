FROM python:3.9-slim

WORKDIR /usr/src/app

COPY senseapp /usr/src/app/senseapp
COPY requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir -r /tmp/requirements.txt

CMD ["python", "senseapp/sense.py"]
