FROM python:3

ENV PYTHONBUFFERED 1

#RUN apk add \
#        --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing \
#	build-base \
#	gdal-dev \
#	musl-dev \
#	zlib-dev \
#	jpeg-dev 

RUN apt-get update && apt-get install --yes libgdal-dev libjpeg-dev

WORKDIR /app
 
COPY . .

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
