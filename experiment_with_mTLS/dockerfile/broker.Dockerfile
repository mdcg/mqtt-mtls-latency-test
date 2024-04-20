from eclipse-mosquitto:2.0.18

WORKDIR /mosquitto/

COPY ./config/mosquitto.conf /mosquitto/config/mosquitto.conf
COPY ./config/pwfile /mosquitto/config/pwfile

COPY ./ca.crt /etc/mosquitto/certs/ca.crt
COPY ./broker.csr /etc/mosquitto/certs/broker.csr
COPY ./broker.crt /etc/mosquitto/certs/broker.crt
COPY ./broker.key /etc/mosquitto/certs/broker.key

RUN chmod a+r /etc/mosquitto/certs/broker.key
