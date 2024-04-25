# This Dockerfile contains the instructions to build 
# an execution environment for the Qiskit.
# When running the container needs the 
# IBMQE_API as an evironment variable to connect to the IBM Quantup Platform

FROM ubuntu:22.04

ENV TZ=America/Mexico_City

ADD ./bin /home/ops/bin

# Install required OS tools & packages for QISKit
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone \
  && apt  update \
  && apt install -y \
    python3-pip \
    python3-psutil \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* \
  && groupadd ops --gid 1001 \
  && useradd --uid 1001 --gid 1001 -s /bin/bash -m ops \
  && chown -Rf ops:ops /home/ops

USER ops

RUN pip install qiskit==0.39.0 qiskit_ibm_provider==0.2.0

WORKDIR /home/ops

ENTRYPOINT ["/home/ops/bin/run.sh"]