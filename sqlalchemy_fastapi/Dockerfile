FROM ubuntu:latest

LABEL maintainer="emanuel.afanador@koombea.com"
LABEL com.amazonaws.sagemaker.capabilities.accept-bind-to-port=true
LABEL com.amazonaws.sagemaker.capabilities.multi-models=true

ARG PYTHON_VERSION=3.8

ENV DEBIAN_FRONTEND noninteractive

# System packages 
RUN apt-get update && apt-get install -y  apt-utils
RUN apt-get update && apt-get install -y --no-install-recommends nginx \
    curl \
    gcc \
    mono-mcs \
    build-essential \
    ca-certificates \
    wget \
    pkg-config 

# Install miniconda and python
RUN curl -L -o ~/miniconda.sh https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && chmod +x ~/miniconda.sh \
    && ~/miniconda.sh -b -p /opt/conda \
    && rm ~/miniconda.sh \
    && /opt/conda/bin/conda update conda \
    && /opt/conda/bin/conda install -y \
        python=$PYTHON_VERSION 

# Add conda to path
ENV PATH=/opt/conda/bin:${PATH}

ARG WORKDIR=/opt/app
WORKDIR ${WORKDIR}

COPY config config
RUN pip install -r config/requirements.txt

COPY . ${WORKDIR}