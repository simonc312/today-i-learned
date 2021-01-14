# Snowball

AWS ships you a physical device (basically like a giant secure usb drive) for you to transfer physically through a direct local connection from your servers to the device. Then the device is shipped with regular carriers like UPS to AWS for upload to an S3 bucket. The snowball device is wiped and sent to another AWS customer.

Sends notifications with SNS
Encryption with KMS

Use cases: when data transfer takes longer than 1 week

## Snowball Edge 

adds computational capabilities like:
- 100 TB storage and 24 vCPU
- 52 vCPU and optional GPU
- supports custom EC2 AMI to perform processing on the go
- supports custom lambda functions

use case: preprocess the data while shipping to be ready to use when it arrives

## AWS Snowmobile 

each has 100 PB of capacity (basically a full size truck)

use case: more than 10 PB of data to transfer

# Direct Connect

Dedicated private connection that avoid public network connections and costs between your servers and AWS
Requires asking a partner to help install the direct connection on your behalf.


use case: 1 to 10 Gbps speeds per connection

