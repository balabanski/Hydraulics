FROM python:3.10 as base

ARG env

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export $(test "${env:-dev}" != "prod" && echo "--with dev") \
    -f requirements.txt \
    --output requirements.txt \
    --without-hashes

FROM python:3.10

COPY --from=base tmp/requirements.txt /code/requirements.txt
# TRY
RUN apt-get update \
    && apt-get -y autoremove \
	&& apt-get clean autoclean \
	&& rm -rf /var/lib/apt/lists/{apt,dpkg,cache,log} /tmp/* /var/tmp/*

WORKDIR /code

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY .. /code/

ENV PYTHONPATH=/code

EXPOSE 8000
