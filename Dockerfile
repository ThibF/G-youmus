FROM debian:latest

RUN apt-get update
RUN apt-get install -qqy ffmpeg
RUN apt-get install -qqy curl
RUN apt-get install -qqy python3-pip
RUN apt install -qqy libxslt-dev libxml2-dev
RUN pip3 install -U setuptools
RUN pip3 install gmusicapi
RUN pip3 install youtube-dl
RUN pip3 install boto3
RUN apt-get install -qqy locales

RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

CMD ["python3", "/src/bin/main.py"]


