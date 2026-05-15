FROM ubuntu:24.04

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        bash \
        can-utils \
        curl \
        file \
        git \
        iproute2 \
        iputils-ping \
        less \
        net-tools \
        procps \
        python3 \
        python3-pip \
        tcpdump \
        vim \
        wget \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY canproxy.py /app/canproxy.py

CMD ["bash", "-lc", "ip link add dev vcan0 type vcan || true; ip link set vcan0 up; python3 /app/canproxy.py client & if [ -t 0 ] && [ -t 1 ]; then exec bash -i; else sleep infinity; fi"]
