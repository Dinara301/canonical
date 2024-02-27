FROM python:3.9

WORKDIR /src

COPY ./requirements.txt /src/requirements.txt

RUN pip install --upgrade pip && pip install -r /src/requirements.txt
COPY . /src
EXPOSE 8000

# Healthcheck to monitor the application
HEALTHCHECK CMD ["curl", "--fail", "http://localhost:8000", "||", "exit 1"]

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]