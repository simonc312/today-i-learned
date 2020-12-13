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
- "ProvisionedThroughputException" if exceeded

### Consumers
Classic
- 2 MB/s at read per shard across all classic consumers
- 5 API calls per shard across all classic consumers

Enhanced Fan Out
- 2 MB/s at read per shard for each EFO consumer
- No API calls needed (push model)

## Kinesis Analytics
Processing on real time stream data (Transform)

## Kinesis Firehose
Deliver **near** real time streams to sources like S3, Redshift, Splunk (Load)
