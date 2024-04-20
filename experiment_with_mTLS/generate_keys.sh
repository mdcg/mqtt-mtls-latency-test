#!/bin/bash
sudo apt-get update
sudo apt-get install openssl

openssl genrsa -des3 -out ca.key 2048;
openssl req -new -x509 -days 1826 -key ca.key -out ca.crt;

openssl genrsa -out broker.key 2048;
openssl req -new -out broker.csr -key broker.key;
openssl x509 -req -in broker.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out broker.crt -days 360;

openssl genrsa -out application.key 2048;
openssl req -new -out application.csr -key application.key;
openssl x509 -req -in application.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out application.crt -days 360
