FROM python:3.12

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/ems

COPY ems ./ems
COPY ems_libs ./ems_libs
COPY pyproject.toml .
COPY README.MD .
COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt
