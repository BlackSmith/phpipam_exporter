FROM python:3.9-slim
ENV WORKDIR /app
WORKDIR $WORKDIR

RUN apt-get update && \
    apt-get install -y --no-install-recommends --no-install-suggests default-mysql-client && \
    apt-get clean

ADD phpipam_exporter/* /app/
ADD poetry.lock /app/poetry.lock
ADD pyproject.toml /app/pyproject.toml

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev --no-root

ENTRYPOINT ["bash"]
