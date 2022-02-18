FROM python:3.10-slim

ARG VERSION=0.5.0

RUN apt-get update -y && \
    apt-get clean

RUN pip install phpipam-exporter==$VERSION

ENTRYPOINT ["phpipam_export"]
