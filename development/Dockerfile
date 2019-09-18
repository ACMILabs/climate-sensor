# base-image for python on any machine using a template variable,
# see more about dockerfile templates here: https://www.balena.io/docs/learn/develop/dockerfile/
FROM balenalib/raspberrypi3-python:3.7-stretch-run

# use `install_packages` if you need to install dependencies,
# for instance if you need git, just uncomment the line below.
RUN install_packages build-essential python-dev python-openssl git

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /code/requirements.txt
COPY ./dev.txt /code/dev.txt
RUN pip install -Ur /code/requirements.txt
ARG IS_LOCAL_ENV
RUN if [ "$IS_LOCAL_ENV" = "true" ]; \
    then pip install -Ur /code/dev.txt; \
    fi
COPY . /code/
WORKDIR /code/

RUN git clone https://github.com/adafruit/Adafruit_Python_DHT.git
WORKDIR /code/Adafruit_Python_DHT/
RUN python setup.py install
WORKDIR /code/

# pi.py will run when container starts up on the device
CMD ["bash","scripts/pi.sh"]
