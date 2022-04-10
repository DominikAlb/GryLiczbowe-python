FROM python:3
MAINTAINER "Dominik Albiniak"

WORKDIR /usr/src/app
RUN apt-get update && \
    apt-get clean

RUN git clone https://github.com/DominikAlb/GryLiczbowe-python

RUN pip3 install --upgrade pip3 && \
    pip3 install aldryn_apphooks_config \
    pip3 install aldryn_apphooks_config \
    pip3 install aldryn_apphooks_config \
    pip3 install aldryn_apphooks_config \
    pip3 install aldryn_apphooks_config \
from typing import List
from datetime import datetime
import statistics as stat
import logging
import os
import random
import matplotlib.pyplot as plt

CMD [ "python3", "GryLiczbowe-python/main.py" ]