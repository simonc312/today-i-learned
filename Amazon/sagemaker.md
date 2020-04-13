# AWS Sagemaker

Resources:

- https://blog.betomorrow.com/keras-in-the-cloud-with-amazon-sagemaker-67cf11fb536

- https://medium.com/weareservian/machine-learning-on-aws-sagemaker-53e1a5e218d9
  - 3 api levels
    - high-level `python-sagemaker-sdk` (cannot be used within aws lambda environment)
    - mid-level `boto3`
    - low-level `awscli+docker` (not covered in article)
    - aws s3 put events do not have 100% delivery guarantee. Safer approach is scheduled step-functions.