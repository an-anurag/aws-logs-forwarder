# AWS Console log forwarder


# What is this?

This is AWS log collector and forwarder. It collects all the AWS console logs in realtime from cloudwatch and 
stores in file and sends to UDP socket over syslog simultaneously. You can configure AWS accounts as many as you want.
This module can fetch logs from multiple CLoudWatch log group and from multiple AWS accounts.


# Prerequisites

   1. Sign up for AWS account
   2. Go to `IAM` and create a IAM user with existing policy `CloudWatchEventsFullAccess`, download the credential file at the last step of user creation.)
   3. Install the `AWS cli` on a host (linux) where you want to deploy the code. (given in the resource dir)
   4. Enter the `aws configure` on the terminal
   5. Enter all the details at prompt such as access key and secret key from a credential file downloaded earlier.
   2. Go to `CloudWatch` in web management console and create a `log-group` and `streams` for each log source.
   3. Go to CloudTrail and create a trail,
   4. Configure trail with log-group to send logs to.
   5. If you want to monitor EC2 instance, then install CloudWatch agent in every instance and configure it.
   6. Create log group for ec2 instance to store logs sent by cloudwatch agent.
   7. Update the `accounts.yaml` file according to your setup done as above.

