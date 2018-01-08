FROM python:2.7-slim

ADD requirements.txt /tmp/

RUN apt-get update
RUN apt-get install -y libfbclient2 \
    && pip install -r /tmp/requirements.txt

# docker build -t ello/python-webapp . -f Dockerfiles/Base.Dockerfile