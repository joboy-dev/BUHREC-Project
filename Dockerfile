FROM python:3.11.5-slim-bullseye

WORKDIR /app
RUN mkdir staticfiles
RUN mkdir media
RUN mkdir media/user
RUN mkdir media/ckuploads

# install system dependencies
RUN apt-get update

# copy all files to docker app file
COPY . /app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python manage.py collectstatic --no-input
RUN python manage.py makemigrations
RUN python manage.py migrate

# create gunicorn log directory
RUN mkdir /var/log/gunicorn

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

EXPOSE 8000

CMD [ "gunicorn", "buhrec_project.wsgi"]