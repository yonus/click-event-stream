FROM python:3.8-slim

WORKDIR /app
COPY ./requirements.txt .
COPY  ./datasource/data /data/click-event-generator
ENV CLICK_EVENT_FILE_DIRECTORY="/data/click-event-generator/clicks"
RUN pip install -r requirements.txt

COPY ./src .
CMD ["python", "main.py"]
