FROM python:3.10.7
WORKDIR /crowd
COPY . /crowd/
RUN pip3 install -r /crowd/requirements.txt
CMD ["celery", "-A", "app.core.celery_app", "worker", "--loglevel=info"]