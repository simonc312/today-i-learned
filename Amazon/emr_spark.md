# EMR with Spark

<img src="./assets/AWS_EMR.png" 
alt="AWS EMR logo" width="80" />

Amazon Elastic MapReduce is a hosted service to help accelerate running data processing applications with packages such as Spark over cluster of ec2 instances.

You can start up EMR clusters like most other Amazon hosted services with Cloudformation templates or Terraform. 

You are charged for the ec2 instances used in the cluster and a base emr service fee per instance per hour. 

Before a cluster is done setting up, you can specify bootstrap steps to perform like installing packages.

After a cluster is set up and enters the waiting status, you can submit emr steps to run commands like spark-submit.

There are a number of metrics available on the EMR manager console which are published to CloudWatch that can be easily integrated to a reporting dashboard such as Grafana.

To handle unexpected data processing loads, you can define an autoscaling policy to scale out the cluster when available running memory drops below certain threshold (for additional task nodes) or when HDFS utilization hits above a certain percentage (for additional core nodes). However, scaling down the cluster when applications are finished running and the cluster becomes idle may require longer time unless some default HDFS configurations are modified for core nodes.

One limitation that has since been fixed as a new feature was not being able to run and execute multiple emr steps in parallel (when a cluster is shared between multiple data processing pipelines). Now since Nov 2019, it is possible to specify a concurrency level for the maximum number of jobs to allow executing in parallel.

Another limitation is the inability to cancel an emr step that has begun running through the aws emr api. Their [help docs tell you to ssh into the emr master node and kill the application directly][1]. 

From the developer's perspective, it would have been nice to be able to stream the logs that are written as the spark application is running through the aws emr api. Trying to read from the s3 output logs (must specify s3 bucket during cluster set up) will never be in realtime and usually are only made available after the entire spark application is completed. 

[1]: https://aws.amazon.com/premiumsupport/knowledge-center/cancel-emr-step/
