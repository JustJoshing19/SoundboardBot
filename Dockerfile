FROM ubuntu:20.04 AS development

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get -y update

# python and poetry

RUN apt-get install -y python3.8 python3.8-dev

RUN apt-get install -y python3-pip

RUN apt-get install -y python-is-python3

RUN pip install poetry

# configure poetry

RUN poetry config virtualenvs.create false

# ffmpeg

RUN apt-get install -y ffmpeg

RUN ffmpeg -version

# build project

COPY ./pyproject.toml ./app/pyproject.toml

WORKDIR /app

RUN poetry install --no-root

COPY . /app

# run project

ENV LOCAL=yes
ENV LOGURU_LEVEL=DEBUG

# local run requires to be built with .env for ease of running

CMD ["poetry","run","python","main.py"]

FROM development AS production

ENV LOCAL=no
ENV LOGURU_LEVEL=INFO

CMD ["poetry","run","python","main.py"]
