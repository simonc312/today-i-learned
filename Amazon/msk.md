# MSK Managed Apache Kafka Service

- alternative to Kinesis
- control plane for Kafka clusters management
- creates and manages broker nodes and Zookeeper nodes
    - choose how many brokers per AZ
    - 1 zookeeper node per AZ
- deploy to VPC and multi AZ (up to 3)
- recovery from common Kafka failures

- default max message size is 1 MB
    - `message.max.bytes` override setting on broker
    - `max.fetch.bytes` override setting on consumer

- latency default is low 10-40ms (way less than Kinesis)
    - can batch message sends with `linger.ms` for higher thoroughput

Encryption with TLS for in-flight between brokers to brokers and clients to brokers
- at rest with KMS for EBS volumes

Authentication with TLS private certificate authority from ACM

Authorization
    - authorize specific security groups for Apache Kafka clients
    - security for clients is done within Apache Kafka cluster not IAM

Monitoring
    - CloudWatch (supports cluster, broker, topic level metrics)
    - Prometheus (JMX or Node Exporter)
    - Broker Log Delivery (S3, Kinesis Firehose)