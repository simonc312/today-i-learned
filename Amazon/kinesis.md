# Kinesis

Basically a managed Apache Kafka service.

Use Cases:
- logs, metrics, IoT data
- real time streaming

Benefits:
- replicates data in 3 availability zones

## Kinesis Streams
Low latency data stream ingestion (Extract)
- default data retention is 24 hours and up to 7 days
- immutable append only data stream
- records are ordered per shard/partition (not globally)
- billed per shard provisioned
- 1 stream can have many shards
- number of shards can change over time (reshard, merge)
- api allows fetching data in batches or per record
- each record's data blob is max 1 MB
- a record's key determines which shard to be sent

### Producers
- 1 MB/s or 1000 records/s at write per shard
- `ProvisionedThroughputException` if exceeded

Data sources:
**SDK**
Method: `PutRecord(s)` single or batch HTTP requests
Use Case: low throughput, higher acceptable latency, simple API, AWS Lambda
- Available on mobile, etc


Other AWS services under the hood use the SDK:
- cloudwatch logs
- kinesis analytics writing back to streams
- aws IoT

**Kinesis Producer Library (KPL)**
Method: C++ or Java library 
Use Case: Long running, high performance producers
- Handles ProvisionedThroughputException errors by retry with exponential backoff
- Synchronous or Asynchronous API
- submits metrics to CloudWatch
- batches by default (write to multiple shards, can aggregate multiple records)
    - based on `RecordMaxBufferedTime` configuration default 100ms 
- CON: Kinesis Consumer Library needed to decode and read records or special helper library
- CON: compression of data not built in 



**Kinesis Agent**
Method: Java agent written on top of KPL
Use Case: runs on servers to collect logs
- preprocess data before sending to streams (single line, csv to json, etc)
- route to multiple streams based on directory/files
- handles file rotation, retry, cloudwatch metrics

- Spark, NiFi, Kafka Connect

### Consumers
Classic
- 2 MB/s at read per shard across all classic consumers
- 5 API calls per shard across all classic consumers

**SDK**
GetRecord(s)

**KCL**
Method: Java first library (available in Go, Python, Ruby, Node, .NET, etc)
Use Case: read records produced by KPL
- de-aggregate records, 
- shard discovery mechanism shared as one "group"
- checkpointing feature to resume progress with Dynamdb table
    - one row per shard
    - sychronizes to determine which consumer application in group to consume 
    - provision accordingly or use On-Demand

**Kinesis Connector Library**
Method: Legacy Java Application runs on EC2 (2016)
Use Case: push Kinesis Stream data to other services like S3, Redshift, Elasticsearch, DynamoDB etc.
- usefulness replaced by Kinesis Firehose or AWS Lambda 

**AWS Lambda**
Use Case: lightweight ETL to any destination, trigger alerts in real time
- has library to de-aggregate records from KPL
- configurable batch size to read 

Enhanced Fan Out
- 2 MB/s at read per shard for each EFO consumer
- No API calls needed (push model)

## Kinesis Analytics
Processing on real time stream data (Transform)

## Kinesis Firehose
Deliver **near** real time streams to sources like S3, Redshift, Splunk (Load)
