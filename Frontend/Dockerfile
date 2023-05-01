FROM python:3

WORKDIR /app

ADD . /app/

EXPOSE 80

COPY . /app

RUN pip install -r /app/requirements.txt --no-cache-dir

ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["python3"]

CMD ["/app/website/manage.py", "runserver", "0.0.0.0:80"]