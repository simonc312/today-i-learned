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
- latency ~200ms


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
- feature released August 2018
- 2 MB/s at read per shard for each EFO consumer
- No API calls needed (push model)
- subscribeToShard() push data model over HTTP/2
- Reduced latency ~70 ms
- Default configuration limits 5 EFO consumers per stream

### Scaling

**Adding Shards or Shard Splitting**
- increase Stream capacity (1 MB/s data per shard)
- divide a "hot shard"
- old shard is closed and deleted once data is expired

**Remove Shards or Shard Merging**
- decrease capacity to save costs
- group two shards with low traffic

[UpdateShardCount API Documentation](https://docs.aws.amazon.com/kinesis/latest/APIReference/API_UpdateShardCount.html)

- Auto Scaling not built in yet
    - expects relying on Auto Scaling + API Gateway + Lambda + storage stage services to trigger UpdateShardCount API
    - [link to aws auto scaling kinesis article](https://aws.amazon.com/blogs/big-data/scaling-amazon-kinesis-data-streams-with-aws-application-auto-scaling/)

**Limitations**
- Resharding cannot be done in parallel. 
    - Ex 1000 shards takes 30K seconds (8.3 hours) to increase to 2000 shards
- can't scale more than 10 times in 24 hours per stream
- can't scale up or down more than 2x current shard count per stream
- default shard limit is 500 for us-west-2 regions
- 10K shards scaling limit

### Security

- IAM policies
- Encryption in flight using HTTPS
- Encryption at rest using KMS
- Client Side encryption is manual
- VPC Endpoints available



## Kinesis Analytics
Processing on real time stream data (Transform)

## Kinesis Firehose
Fully managed service to deliver **near** real time streams to specific compatible sources (Load)

- Automatic scaling
- Data conversions from JSON to Parquet/ORC (only for S3)
- Supports compression for S3 (GZIP, ZIP, and SNAPPY)
- Spark can only read from Kinesis Data Streams not Firehose
- 60 second latency minimum 
- Data sources:
    - Kinesis Producer Library and SDK
    - Kinesis Agent
    - Kinesis Data Streams
    - CloudWatch
    - IoT rules actions

- Data destinations:
    - S3 
    - Redshift (COPY command from S3)
    - ElasticSearch
    - Splunk

- can work with Lambda for transformation
- can specify optional Transformation and Delivery failures to S3 bucket with error path prefix
- in exercise for data published from Kinesis Agent to S3 the batches were automatically partitioned by publish date
    - buffer size translates to S3 file size when data arrives faster than time rules

**Buffer Sizing**
- accumulates records in buffer
- based on buffer size (>=1.2 MB) and time rules (>= 60 seconds and <= 900 seconds)
- Ex 32 MB or 2 minutes thresholds
- can automatically increase buffer size to increase throughput
- no data storage
