# AWS IoT Internet of Things

## Thing Registry

## Device Gateway

Enables smart device to securely communicate with AWS. Acts as intermediary between devices.

## IoT Message Broker

## IoT Rules Engine

Dispatches messages from broker to various targets like Kinesis, SQS, Lambda, etc. 
- Allows for overriding behaviors between messages 

## Device Shadow

Maintains same expected state as real smart device.
Instructs updates through message broker, through device gateway, and back to real IoT Thing parameters when Thing returns from offline to online.