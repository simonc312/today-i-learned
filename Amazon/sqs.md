# AWS SQS

- oldest offering (over 10 years old)
- fully managed
- scales from 1 msg/sec to 10ks /sec
- Default retention: 4 days to 14 days max
- Low latency (<10 ms on publish and receive)
- Horizontal scaling of consumers
- At least once delivery (so duplicates possible)
- Can have out of order messages (best effort ordering)
- Limit of 256KB per message body sent

## Producing Messages

- define Body up to 256kb string
- add optional message key values attributes (metadata)
- provide optional delivery delay 
- response returns message id and MD5 hash of body

## Consuming Messages 

- poll SQS (10 messages at a time)
- process messages within visibility timeout
- cannot process same message by multiple consumer applications
- delete messages from SQS using message ID and receipt handle

## FIFO Queue

- name of queue msut end in .fifo
- lower throughput (3K/sec soft limit with batching 300/s without)
Messages are processed in order by consumer
- messages sent exactly once
- 5-minute interval de-duplication using "Duplication ID"
- ordering based on optional Group ID

## SQS Extended Client 

- send large messages to S3
- send small metadata message to SQS 
- consumer uses metadata to fetch large message from S3

## Use Cases
- Decouple applications for asynchronous processing
    - payments
    - database writes
    - emails
    - order and image processing

- Autoscaling possible

## Limits

- Max 120K in-flight messages processed by consumers
- Message content is text (JSON, XML, etc)
- Batch Request max of 10 messages - max 256KB
- Standard Queue have unlimited Throughput
- Data Retention 1 minute to 14 days
- Once read message is deleted by consumer

## Security 

- Encryption in flight with HTTPS
- Encryption at rest with Server Side Encryption using KMS manged customer master keys (CMKs) for message body only
    - excludes Queue metadata
    - excludes Message metadata
    - per queue metrics
    - does not apply encryption to existing messages
- IAM policy 
- SQS queue access policy


Example by IP

```
{
   "Version": "2012-10-17",
   "Id": "Queue1_Policy_UUID",
   "Statement": [{
      "Sid":"Queue1_AnonymousAccess_AllActions_AllowlistIP",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "sqs:*",
      "Resource": "arn:aws:sqs:*:111122223333:queue1",
      "Condition" : {
         "IpAddress" : {
            "aws:SourceIp":"192.168.143.0/24"
         }
      }
   }]
}
```

Example by datetime conditions: 
```
{
   "Version": "2012-10-17",
   "Id": "Queue1_Policy_UUID",
   "Statement": [{
      "Sid":"Queue1_AnonymousAccess_ReceiveMessage_TimeLimit",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "sqs:ReceiveMessage",
      "Resource": "arn:aws:sqs:*:111122223333:queue1",
      "Condition" : {
         "DateGreaterThan" : {
            "aws:CurrentTime":"2009-01-31T12:00Z"
         },
         "DateLessThan" : {
            "aws:CurrentTime":"2009-01-31T15:00Z"
         }
      }
   }]
}
```

