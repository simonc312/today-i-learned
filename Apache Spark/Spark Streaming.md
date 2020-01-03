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





