FROM python:3
MAINTAINER "Dominik Albiniak"

WORKDIR /usr/src/app
RUN apt-get update && \
    apt-get clean

RUN git clone https://github.com/DominikAlb/GryLiczbowe
CMD [ "python3", "GryLiczbowe/main.py" ]