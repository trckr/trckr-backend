FROM python:3

ENV PYTHONBUFFERED 1
RUN mkdir /code
WORKDIR /code

ADD requirements.txt /code/
RUN pip install -r requirements.txt

ADD . /code/

# RUN python3 manage.py migrate

CMD python manage.py runserver 0.0.0.0:8000
