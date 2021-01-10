# AWS IoT Internet of Things

## Thing Registry

All connected IoT devices are catalogued. 
- X.509 certificates for each device to connect to AWS (optionally for authentication)
- IoT Groups like IaM Groups
- IoT Policies are JSON docs

## Device Gateway

Enables smart device to securely communicate with AWS. Acts as intermediary between devices.

- supports MQTT, WebSockets, HTTP 1.1
- Fully managed and autoscales
- marketed to support over 1 billion devices

## IoT Message Broker

- Pub/Sub messaging pattern - low latency
- messages are published into topics
- broker forwards messages to all clients connected to the topic

## IoT Rules Engine

Dispatches messages from broker to various targets like Kinesis, SQS, Lambda, etc. 
- Allows for overriding behaviors between messages 

- Rules are defined on MQTT Topics
- Rules need IAM roles to perform their actions
- Ex Save a file to S3

## Device Shadow

Maintains same expected state as real smart device.
Instructs updates through message broker, through device gateway, and back to real IoT Thing parameters when Thing returns from offline to online.

State of IoT device represented by a JSON doc

## IoT Greengrass

- brings compute layer to device locally
- execute AWS Lambda functions on devices
    - pre-process data
    - execute preditions based on ML models
    - keep device data in sync
    - communicate between local devices
    - operate offline