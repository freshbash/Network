FROM python:3
COPY . /usr/src/app
WORKDIR /usr/src/app
RUN pip3 install django
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]