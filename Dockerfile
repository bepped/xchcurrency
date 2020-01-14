FROM python:3.7.2-slim

ENV FLASK_APP xchcurrency.py
ENV FLASK_CONFIG production

RUN adduser xchcurrency
USER xchcurrency

WORKDIR /home/xchcurrency

#RUN apk add --no-cache make build-base libffi-dev
     
COPY requirements.txt requirements.txt
RUN python -m venv venv

RUN venv/bin/pip install --upgrade pip
RUN venv/bin/pip install -r requirements.txt

COPY app app
COPY xchcurrency.py config.py boot.sh ./

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
