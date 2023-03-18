# Spark Streaming

Notes gathered from *Stream Processing with Apache Spark* by Gerard Maas and Francois Garillot (published July 2019). 


### Chapter 1 

<img src="./assets/spark_abstraction_layers.png" 
alt="Spark Abstraction Layers" width="300" />

There are 2 streaming APIs offered by Spark. 
- **Spark Streaming** was the first built on top of core Spark engine. Introduced in version 0.7.0 in Feb 2013. Exposes DStream or Discretized Stream model.
- **Structured Streaming** is built on top of Spark SQL layer. It extends the Dataset and DataFrame APIs. Introduced in version 2.0 in July 2016. 

The default Structured Streaming implementation uses a microbatch approach execution model. This is not suitable for applications that require more than minimum latency between microbatches which can be in seconds to milliseconds range.

An experimental model supports near-real-time continuous execution modes. 

### Chapter 2

The functional programming quality of declaring the transformations and aggregations on *immutable data streams* can be used to reproduce the entire pipeline of changes applied from data source to data sink.

- **Tumbling Windows** aggregate events into independent non-overlapping buckets. Where the window length is equal to the reporting frequency. Ex. "the total number of clicks per hour"

- **Sliding Windows** aggregate events based on the window length and a higher reporting frequency. Ex "the average share price over the last day reported hourly" 

Stateful Stream processing is needed when incoming data is used to compute existing internal state. This state can also affect the output of operations on incoming data. Ex. Fraud Detection of credit card transactions use new transaction data to categorize if fraudulent and also adjust internal model weights.

When storing internal state for streaming processing application, you must ensure it is not proportional to the unbounded amount of incoming data. However much available memory resources will eventually hit limits when the internal state depends on such cases. 

Proper timestamping of data is essential for proper reordering of events from data streams to produce accurate history logs. In addition to an *Event Time* produced by original data source, a *Processing Time* can be produced by the processing system. Currently only Structured Streaming provides native support for event-time processing (handling of delayed stream elements).

When trying to define windows based on event time, an adjustable *watermark* (oldest timestamp accepted) is used to limit the potentially unbounded time it would take to process all events if there are expected events that are missing/dropped or late. Users must carefully decide how to set watermarks as too short a duration would cut off data stream window from meaningful results - while too large a duration would cause excessive delays in waiting for events that are unlikely to appear and prevent further processing.

### Chapter 3

- *Lambda architecture* duplicates a streaming application with a batch equivalent running parallel. Ex. end of day batch sync while streaming updates multiple times a day. The batch dataset also serves as benchmark for performance and data quality especially if tied to revenue. The difficulty of this architecture is having 2 life cycles to maintain and avoid causing duplicates. The book appears to treat this as a transition phase where a legacy batch application is reliable and more predictable - when adding streaming pipeline as experiment.

- *Kappa architecture* purely streaming pipeline. No reliance on a batch model. Ex. each sink of pipeline is consumed as source of next stage. If there is no stateful processing done - no accumulation of events - and each event is transformed independently - it is inevitable for stream version to perform worse than batch version which can sort and aggregate the batch of data. The book implies that heuristics applied to an online streaming app is generally worse off than a batch app operating with more data.

### Chapter 4. Apache Spark as Stream Processing Engine

- In Memory Usage and short term caching of previous stages and spilling over to secondary storage during peak loads
- Failure Recovery - of task assigned to executor can be retried from last successful stage to a different executor. 
- Lazy Evaluation - last output operation triggers execution in cluster

Unlike some stream processors like Apache Flink or Apache Storm, Spark is an equal opportunity processor and delays all data elements for at most one batch interval period before acting on them where the smallest interval can be a 1 second period. Where Spark shines is being able to process large batches of data quickly.

When running a 24/7 streaming application the resiliency of automatic retries on failure is crucical. It also becomes necessary to operate on a multi-tenant model where resources must be shared between streaming applications. 

### Chapter 5. Distributed Processing Model

Cluster Managers are responsible for assigning tasks among pool of available healthy workers and securely isolating the user applications if several share infrastructure in a multi-tenant arrangement. 

Kubernetes is the newest cluster manager available to interact with Spark jobs.

Apache Spark includes its own local and standalone cluster manager, but it is not recommended for using in production. It is more useful for Spark developers to work in a barebones environment without bells and whistles. It does not even distribute/provision .jar files to new worker nodes.

Depending on the cluster manager used to orchestrate Spark jobs, the executors can be fulfilled by individual processes, containers, and virtual machines. 

Spark's microbatch approach comes from Bulk Synchronous Parallelism (BSP). There is a split distribution of asynchronous work in parallel defined as a stage by the driver. There is a defined fixed regular time interval where a global check is made like a heartbeat to poll if the stage is completed by all workers.

In contrast, *record one-at-a-time* processing paradigm has lower latency because it reacts without the need to complete some global checkpointing. 

Similar to the comparision with rent vs buy problems, microbatching offers more details on how to proceed in fault tolerance because of checkpointed stages. It can scale up and down resources between stages. 

Spark Streaming's default internal execution model uses a dynamic batch interval that attempts to process new batch as soon as previous one has been processed. 

Processing Model:
1. Update data read from source - fetching start and end offsets of current batch
2. logical planning and query planning
3. launch and schedule computation to update continuous query to refresh

### Chapter 6 Resilience Model

*Resilient Distributed Datasets* (RDDs) are the foundation for strong fault tolerance guarantees. 

<img src="./assets/RDD_DAG.png" 
alt="Spark Abstraction Layers" width="400" />

User application code is interpreted and used to generate an internal RDD Directed Acyclic Graph (DAG).

<img src="./assets/spark_stage.png" 
alt="Spark Abstraction Layers" width="400" />

This is a very useful diagram that highlights how partitions of an RDD are processed by different executors. A stage can be comprised of multiple tasks be are marked by boundaries such as operations that require data reshuffling. Stages are executed in sequence.

- Task failures are restarted by new executor with previous stage data fetched by an executor that participated in shuffle or if cached to memory or disk explicitly with persist(). These are the most common failures due to it being the lowest level.
- Stage failures are retried by shuffling service that is intended to be long running and reliably performs data transfers with a netty backend in Java. It runs as a separate process in all cluster modes.
- Driver failures can be restarted from last known state through checkingpointing option `sparkContext.setCheckpointDirectory()` to reliable distributed storage. In cluster mode, the driver can be automatically restarted but not in client mode. 

### Chapter 7 Introducing Structured Streaming 

The *Dataset* abstraction in Spark SQL is useful for data with defined schema and offers type-safe collection operations. 

The *Dataframe* API is like Python Pandas and R Dataframes is intended to support modern data engineering and data science practices. 

We can appreciate how uniform the Dataframe API can be applied to both batch and streaming applications. 

Queries with streaming sources must be executed with `writeStream.start()`. It will return a *StreamingQuery* instance to use for pausing, stopping, or starting the stream. Allows us to run multiple streams in same spark session.

The outputMode must be specified by the writeStream:
- "complete" outputs entire query over table each time new data is processed
- "update" outputs only rows of table that have been modified or are new since last trigger. Only meaningful for aggregation queries
- "append" is default mode that only outputs new immutable rows added to result table. Guarantees each result will output only once. If used with an aggregation a watermark needs to be defined.

Not all modes are supported by every type of query. 
For more information see: https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html#output-modes

---

### Chapter 8 - The Structured Streaming Programming Model 


> Thanks to the intermediate query representation used in Spark SQL, the performance of the programs is identical regardless of the *language binding* used.

> Creating a streaming *DataFrame* does not result in any data actually being consumed or processed until the stream is materialized. This requires a query...

As a testing data source format, *"rate"* can be used to generate a stream of rows at the rate given by rowsPerSecond option.

API operations that require immediate materialization are not directly supported on streams like:
- count
- show
- take(n)
- describe
- distinct
- foreach
- sort

Some operations like sort and count require an aggregation query to be defined first. 

Alternative to foreach is output with *foreach sink*.
Alternative to show is to output with *console sink*.

Specifying the *trigger option* to *ProcessingTime(interval)* dictates the frequency of query results in microbatch model.

Specifying the *trigger option* to *Continuous(checkpoint-interval)* switches execution engine to experimental continuous engine for low-latency processing. 

### Chapter 9 - Structured Streaming in Action

A streaming Dataset will return `isStreaming` true.

An Apache Kafka Dataset will have a fixed schema:
- key
- value
- topic
- partition
- offset
- timestamp
- timestampType

Only when `dataSet.start()` is called will consumption of the stream begin and query operations materialize.

```
query = dataSet.writeStream
  .outputMode('append')
  .format('parquet')
  .option('path', targetPath)
  .option('checkpointLocation', checkpointPath)
  .start()
```

To output events that have been processed recently, 
call `query.recentProgress()`. When the results return with attribute `numInputRows` that is nonzero, it means the job is consuming data.

### Chapter 10 - Structured Streaming Sources

The streaming data source is informed that data has been processed by commiting a given offset. This contract establishes that all data before the committed offset has been processed and subsequent requests will only be for greater offsets. Sources may opt to discard previous data to release resources. 

To recover from eventual failure, offsets are checkpointed to an external storage. 

Data sources must also be relayable in the same order
and provide a schema. 

Spark Structured Streaming delegates recovery responsibility to the source. 

Examples of unreliable sources are the built-in `Socket` and `Rate` sources.

The book suggests to avoid the complexity of keeping schema definitions up to date when using Scala, to use the inference method when possible. However, that would produce issues down the road in an ETL pipeline. 

The file based streaming data source formats supported are the same as static Dataframe, Dataset, and SQL APIs: 
- CSV
- JSON
- Parquet
- ORC
- text
- textFile

CSV handling of corrupt data or unexpected schema has a `PERMISSIVE` mode option which sets all expected fields to null and stores the entire corrupted value as string with `columnNameOfCorruptRecord` option specified.  

The default `multiLine` option is set to false for the JSON format parser. Spark expects each line of the JSON file to be a different record. 

To create a streaming source from Parquet files, you only need to specify the schema and directory location. 

To create a streaming source from Kafka, you only need to specify the host:port (`kafka.bootstrap.servers`) of the Kafka broker(s), the topic(s) which to subscribe and consume events from, and the `checkpointLocation` to keep track of consumed offsets.  

The `startingOffsets` option is only used the first time a query is made. All future runs will rely on the checkpoint information stored. Clearing the checkpoint contents is required to restart from a specific offset. 

Many additional standard configurations used by kafka can be set by prefixing with `kafka`. Such as `kafka.ssl.truststore.location` or `kafka.ssl.key.password`. 

There are certain configurations that cannot be overridden because they could conflict with internal process of the source. 
- `auto.offset.reset`
- `enable.auto.commit`
- `group.id`
- `key.deserializer`
- `value.deserializer`
- `interceptor.classes`

### Chapter 11 - Structured Streaming Sinks

To participate in end to end reliable data delivery, sinks must provide an *idempotent* write operation. 

The combination of a replayable source and an idempotent sink is what allows Structured Streaming to be *exactly once* semantic guarantees. 

Built-in reliable sinks:
- File sink 
  - local fs/hdfs/s3 formats are same as File source
  - these files can become part of a data lake
  - treat as data at rest
  - only supports *append* output mode
  - specify *checkpointLocation* 
  - specify destionation *path*
  - specify trigger to avoid generation of many small files
  - specify data columns as partitions if want to change local default matching number of cores
  - specify *compression* format (default is None)

- Kafka sink 
  - continue processing data as stream
  - when publishing the key determines the partition of topic
  - similar to distribution key for redshift table
  - null value key will use round robin assignment 
  - specify *topic* per data row to implement fan-out approach to sort incoming records for further processing
  - encoding the payload with a schema definition like with AVRO allows for creation of artifacts in different languages and ensures data can be consumed later on


Nonreliable sinks for local development/tests:
- Memory sink (temporary table that can be queried within same JVM process)
- Console sink (prints results to stdout)

How to create a custom sink?

The *foreach* sink consists of an API and sink definition that provides access to results of the query execution. The *ForeachWriter* class (must be Serializable else errors will be thrown) contains 3 abstract methods to define:
- open(partitionId: Long, version: Long): Boolean
  - called every trigger interval
  - decide to process the partition offered by returning true
- process(value: T): Unit
  - given access to data unit
  - function must produce side effect such as writing to a DB, calling a REST API
- close(errorOrNull: Throwable): Unit
  - null object if output terminated successfully for partition 
  - called at end of every partition writing operation
  - must write/commit partition/version combinations already processed successfully

The *ForeachWriter* is executed as separate instances on each node of the cluster that contains a partition of the streaming data. 

### Spark 3.2 Improvements

Spark now supports [RocksDB](https://github.com/facebook/rocksdb/wiki/RocksDB-Overview), a persistent key value store for performant state management. RocksDB offers significant boosts in both lookup performance and latency compared to the legacy, in-memory solution. To run your Spark Application with RocksDB add the following configuration setting:

    “spark.sql.streaming.stateStore.providerClass”: “org.apache.spark.sql.execution.streaming.state.RocksDbStateStoreProvider”


Koalas, the Spark implementation of the popular Pandas library, has been growing in popularity as the go-to transformation library for PySpark. Koalas will now be bundled with Spark by default, it does not need to be installed as an additional library. This makes it super easy for data scientists used to pandas to transition to spark and take advantage of the distributed processing features for supporting large datasets. [Migration details](https://spark.apache.org/docs/latest/api/python/migration_guide/koalas_to_pyspark.html)

    from pyspark.pandas import read_csv
    spark_df = read_csv('file_path)

PySpark Pandas now uses [plotly](https://plotly.com/python/) by default. Plotly offers a number of enhancements such as native support for interactively zooming in and out of the graph, as well as recomputing plot views using Spark. If you choose to switch back to matplotlib, you can specify the PySpark plotting library in your Spark config.

### Spark 3.3 Improvements & Breaking Changes

Drop support of Python 3.6 - Require 3.7+

upgrades to Kafka 3.1.0
upgrades log4j 1 to 2
support for running on Apple Silicon and Java 17

DataStream Writer Trigger new option
*availableNow* bool, optional

    if set to True, set a trigger that processes all available data in multiple batches then terminates the query. Only one trigger can be set.

solves issue of the driver trying to process all available data in one batch and running into JVM OOM.