FROM python:3

# Install netcat for ip route
RUN apt-get update \
 && apt-get install -y netcat \
 && rm -rf /var/lib/apt/lists/*

 # Use an optional pip cache to speed development
RUN export HOST_IP=$(ip route| awk '/^default/ {print $3}') \
 && mkdir -p ~/.pip \
 && echo [global] >> ~/.pip/pip.conf \
 && echo extra-index-url = http://$HOST_IP:3141/app/dev/+simple >> ~/.pip/pip.conf \
 && echo [install] >> ~/.pip/pip.conf \
 && echo trusted-host = $HOST_IP >> ~/.pip/pip.conf \
 && cat ~/.pip/pip.conf

RUN cat ~/.pip/pip.conf

ADD . /root

RUN pip install -r /root/requirements.txt


CMD ["python", "/data/main.py"]