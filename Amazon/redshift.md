# Redshift

Redshift is an AWS hosted database as a service based on Postgresql but highly scalable to Petabytes of data. This service is charged per instance/hour and is not billed by amount of data processed per query like Snowflake. Storage and compute resources are lumped together. So if a Redshift cluster is inactive for 23 out of 24 hrs it is billed the same as if it was active all 24 hours. 


When creating a cluster you can specify the instance types of each worker node. A single cluster without requesting for upgrade is limited to ~20 workers.

Choosing distribution keys is very important because it will impact any queries that require copying data from different workers to same location. Optimal distribution keys do not create data skew between workers and are shared between many tables as common join key. Usually they will have high cardinality to reduce chance of data skew.

Data is stored in columnar format for better compression and access for selective column based queries. By default most table columns are compressed with lzo encoding unless its specified as a sort key or primary key. 

Amazon will run VACUUM commands for cleaning up deleted rows, but you will be responsible for running VACUUM commands that also perform sorting. One of the major pain points of Redshift is attempting to query a large unsorted table. This can occur if tables are not routinely sorted but constantly updated with fresh data from a batch scheduler.

Unlike some database systems, there are no such things as materialized views. Views in Redshift are simply stored select statements that execute at runtime and are not persisted in storage. 

Redshift Spectrum is a relatively new option for querying data from AWS S3 as it it existed as an external table. This is useful for allowing infrequently accessed data to be stored in a data lake in S3 to reduce Redshift storage costs.

