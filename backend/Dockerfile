FROM python:3.12.0a2-alpine3.17

WORKDIR /app

RUN apk add gcc musl-dev libffi-dev mariadb-connector-c-dev

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

EXPOSE 5000

CMD [ "/bin/ash", "-c", "flask --app app.py --debug run --host 0.0.0.0" ]