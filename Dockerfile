FROM ubuntu:14.04
MAINTAINER Vishal Lall "vishal.h.lall@gmail.com"
RUN apt-get update && apt-get install -y software-properties-common
RUN add-apt-repository ppa:webupd8team/java
RUN echo debconf shared/accepted-oracle-license-v1-1 select true | \
        sudo debconf-set-selections

RUN apt-get update && apt-get install -y \
        python \
        build-essential \
        python-dev \
        python-pip \
        git \
        wget \
        oracle-java8-installer

RUN \
  pip install elasticsearch \
  numpy \
  pandas \
  flask \
  Flask-Limiter \
  Flask-API \
  requests \
  Pympler

WORKDIR /home

RUN \
  wget "https://download.elasticsearch.org/elasticsearch/release/org/elasticsearch/distribution/deb/elasticsearch/2.2.0/elasticsearch-2.2.0.deb" -O elasticsearch-2.2.0.deb && \
  dpkg -i elasticsearch-2.2.0.deb && \
  git clone https://github.com/vlall/darksearch

COPY entrypoint.sh /home/

CMD /home/entrypoint.sh
