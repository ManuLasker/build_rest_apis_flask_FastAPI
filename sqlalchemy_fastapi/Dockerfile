FROM tiangolo/uvicorn-gunicorn-fastapi

RUN apt-get update -y

RUN pip install fastapi[all]

ARG WORKDIR=/opt/app
WORKDIR ${WORKDIR}

# COPY src ${WORKDIR}/src
# COPY templates ${WORKDIR}/templates