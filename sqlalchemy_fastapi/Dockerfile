FROM tiangolo/uvicorn-gunicorn-fastapi

RUN apt-get update -y

ARG WORKDIR=/opt/app
WORKDIR ${WORKDIR}

COPY config config
RUN pip install -r config/requirements.txt

# COPY src ${WORKDIR}/src