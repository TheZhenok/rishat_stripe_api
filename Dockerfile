FROM python:3.11.2-buster

WORKDIR /app

COPY . .

RUN pip install -r tools/requirements/base.txt
RUN python3 manage.py makemigrations
RUN python3 manage.py migrate
RUN python3 manage.py test orders

EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]