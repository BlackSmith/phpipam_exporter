FROM python:3.9-slim

ARG VERSION=0.2.0

RUN apt-get update && \
    apt-get clean

RUN pip install phpipam-exporter==$VERSION

ENTRYPOINT ["phpipam_export"]
