FROM ubuntu:18.04
ENV PATH="/root/miniconda3/bin:${PATH}"
ARG PATH="/root/miniconda3/bin:${PATH}"
RUN apt-get update
RUN apt-get install -y build-essential
RUN apt-get install -y wget && rm -rf /var/lib/apt/lists/*

# Getting miniconda
RUN wget \
    https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && mkdir /root/.conda \
    && bash Miniconda3-latest-Linux-x86_64.sh -b \
    && rm -f Miniconda3-latest-Linux-x86_64.sh
RUN conda --version

#RUN conda install -c conda-forge libgdal

# Getting node
RUN conda install -c conda-forge nodejs
RUN python -V

# Copy files from the project
COPY . /app
WORKDIR /app

# Install node dependencies
RUN npm install

# Install python dependences
RUN pip install -r requirements/local.txt

# Build asset pipeline



# Collect static
RUN python manage.py collectstatic

# create the appropriate directories
RUN mkdir /static

#  Clear /static, copy static into static folder then run the server
ENTRYPOINT rm -rf /static/* \
    && cp -r /app/staticfiles/* /static \
    && cd /app && gunicorn --bind 0.0.0.0:8000 config.wsgi
