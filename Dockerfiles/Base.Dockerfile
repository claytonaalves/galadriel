FROM python:3.7-slim

ADD requirements.txt /tmp/
ADD requirements-prod.txt /tmp/

RUN apt-get update
RUN apt-get install -y libfbclient2 \
    && pip install -r /tmp/requirements.txt \
    && pip install -r /tmp/requirements-prod.txt

# docker build -t ello/python-webapp . -f Dockerfiles/Base.Dockerfile
