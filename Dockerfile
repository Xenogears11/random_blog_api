FROM python:3.5-alpine

WORKDIR /app

COPY . /app

RUN apk update \
  && apk add --virtual build-deps gcc python3-dev musl-dev \
  && apk add postgresql-dev \
  && pip install psycopg2 \
  && apk del build-deps

RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 8888

CMD ["python", "api/main.py"]
