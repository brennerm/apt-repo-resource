ARG base_image=python:3.6-alpine

FROM ${base_image}

RUN pip install apt-repo packaging

COPY scripts/check.py /opt/resource/check
COPY scripts/in.py /opt/resource/in
COPY scripts/out.py /opt/resource/out
RUN chmod +x /opt/resource/check /opt/resource/in /opt/resource/out
WORKDIR /opt/resource