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

