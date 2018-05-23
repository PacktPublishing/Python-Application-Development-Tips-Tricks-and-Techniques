FROM python:3

RUN mkdir -p /usr/app
WORKDIR /usr/app

ADD requirements.txt /usr/app
RUN pip install -r requirements.txt

ADD . /usr/app

EXPOSE 8000

CMD [ "gunicorn", "-b", "0.0.0.0:8000", "main:app" ]

