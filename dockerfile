FROM python:3.10.7
WORKDIR /crowd
COPY . /crowd/
RUN pip3 install -r /crowd/requirements.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]