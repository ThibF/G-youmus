FROM debian:latest

RUN apt-get update
RUN apt-get install -qqy ffmpeg
RUN apt-get install -qqy curl
RUN apt-get install -qqy python3-pip
RUN pip3 install gmusicapi youtube-dl
RUN pip3 install boto3

CMD ["python3", "/src/bin/consumerSQS/consumer.py"]


