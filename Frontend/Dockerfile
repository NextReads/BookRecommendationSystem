FROM python:3

WORKDIR /app

ADD . /app/

EXPOSE 80

COPY requirements.txt /app

RUN pip3 install -r requirements.txt --no-cache-dir

COPY . /app

ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["python3"]

CMD ["/app/website/manage.py", "runserver", "0.0.0.0:80"]