FROM ubuntu:xenial

RUN apt-get update && apt-get install -y python3-apt

COPY scripts/check.py /opt/resource/check
COPY scripts/in.py /opt/resource/in
COPY scripts/out.py /opt/resource/out
COPY scripts/common.py /opt/resource/common.py
RUN chmod +x /opt/resource/check /opt/resource/in /opt/resource/out
WORKDIR /opt/resource