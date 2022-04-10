FROM python:3
MAINTAINER "Dominik Albiniak"

WORKDIR /usr/src/app
RUN apt-get update && \
    apt-get clean

RUN git clone https://github.com/DominikAlb/GryLiczbowe-python

RUN pip3 install --upgrade pip && \
    pip3 install matplotlib

CMD [ "python3", "GryLiczbowe-python/main.py" ]