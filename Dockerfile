FROM python:3

ENV PYTHONBUFFERED 1
ENV RH_DOCKER 1

WORKDIR /install
RUN apt-get update && apt-get install --yes libgdal-dev libjpeg-dev

COPY requirements_docker.txt .

RUN pip install -r requirements_docker.txt

VOLUME /data

WORKDIR /usr/src/app

COPY . .

EXPOSE 8000

CMD ["bash", "docker_run.sh"]
