# Spark Streaming

Notes gathered from *Stream Processing with Apache Spark* by Gerard Maas and Francois Garillot (published July 2019). 

<img src="./assets/spark_abstraction_layers.png" 
alt="Spark Abstraction Layers" width="300" />

There are 2 streaming APIs offered by Spark. 
- **Spark Streaming** was the first built on top of core Spark engine. Introduced in version 0.7.0 in Feb 2013. Exposes DStream or Discretized Stream model.
- **Structured Streaming** is built on top of Spark SQL layer. It extends the Dataset and DataFrame APIs. Introduced in version 2.0 in July 2016. 

The default Structured Streaming implementation uses a microbatch approach execution model. This is not suitable for applications that require more than minimum latency between microbatches which can be in seconds to milliseconds range.



An experimental model supports near-real-time continuous execution modes. 