FROM python:3

WORKDIR /app

EXPOSE 80

COPY ./Frontend /app

RUN pip install -r requirements.txt --no-cache-dir

ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["python3"]

CMD ["/app/website/manage.py", "runserver", "0.0.0.0:80"]