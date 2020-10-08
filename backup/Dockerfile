FROM python:3 as development

# Ensures that the python output is sent straight to terminal
ENV PYTHONBUFFERED 1

WORKDIR /opt/reprohack

COPY requirements.txt ./

RUN apt-get update && apt-get install --yes libgdal-dev libjpeg-dev && python -m pip install -r requirements.txt

EXPOSE 8000

LABEL   version="1.0.0-development" \
        description="Reprohack (Django) web site" \
        maintainer="a.krystalli@sheffield.ac.uk"

FROM development as production
COPY . ./
LABEL   version="1.0.0-production"
