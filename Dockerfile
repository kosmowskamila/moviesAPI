FROM python:3.8
ENV PYTHONBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY . /code/
RUN python manage.py collectstatic --noinput --clear

CMD gunicorn movies.wsgi:application --bind 0.0.0.0:$PORT