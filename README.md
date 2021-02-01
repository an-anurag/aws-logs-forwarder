# AWS Console log forwarder


# What is this?

This is AWS log collector and forwarder. It collects all the AWS console logs in realtime from cloudwatch and 
stores in file and sends to UDP socket over syslog simultaneously. You can configure AWS accounts as many as you want.
This module can fetch logs from multiple CLoudWatch log group and from multiple AWS accounts.


# Prerequisites

   1. Sign up for AWS account
   2. Go to `IAM` and create a IAM user with existing policy `CloudWatchEventsFullAccess`, download the credential file at the last step of user creation. [see creating IAM user](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwi2--bFhZvqAhVC4XMBHUP2CwwQFjAAegQIBBAB&url=https%3A%2F%2Fdocs.aws.amazon.com%2FIAM%2Flatest%2FUserGuide%2Fid_users_create.html&usg=AOvVaw1QBSa1KvEcA6W3pn9hJfzn)
   3. Install the `AWS cli` on a host (linux) where you want to deploy the code. (given in the resource dir)
   4. Enter the `aws configure` on the terminal
   5. Enter all the details at prompt such as access key and secret key from credential file downloaded earlier.
   2. Go to `CloudWatch` in web management console and create a `log-group` and `streams` for each log source. [see creating log group](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwilt6qvhZvqAhXlyzgGHRVsDvcQFjABegQIDBAD&url=https%3A%2F%2Fdocs.aws.amazon.com%2FAmazonCloudWatch%2Flatest%2Flogs%2FWorking-with-log-groups-and-streams.html%23%3A~%3Atext%3DTo%2520create%2520a%2520log%2520group%2Cthen%2520choose%2520Create%2520log%2520group.&usg=AOvVaw2lL2qcHRVtpOur6tSUV8Qp)
   3. Go to CloudTrail and create a trail, [see creating trail](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwi16NTxhJvqAhWd93MBHdpnBK0QFjABegQIDRAD&url=https%3A%2F%2Fdocs.aws.amazon.com%2Fawscloudtrail%2Flatest%2Fuserguide%2Fcloudtrail-create-a-trail-using-the-console-first-time.html%23%3A~%3Atext%3DTo%2520create%2520a%2520CloudTrail%2520trail%2520with%2520the%2520AWS%2520Management%2520Console%26text%3DChoose%2520the%2520AWS%2520Region%2520where%2CChoose%2520Get%2520Started%2520Now.%26text%3DIf%2520you%2520do%2520not%2520see%2Ca%2520name%2520for%2520your%2520trail.&usg=AOvVaw1uvcfOEFwcgGR2ZNTDMBTB)
   4. Configure trail with log-group to send logs to.
   5. If you want to monitor EC2 instance, then install CloudWatch agent in every instance and configure it. [see install CW-agent](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwib9sOFhpvqAhWXbn0KHexhACQQFjAAegQIAhAB&url=https%3A%2F%2Fdocs.aws.amazon.com%2FAmazonCloudWatch%2Flatest%2Fmonitoring%2Finstall-CloudWatch-Agent-on-EC2-Instance.html&usg=AOvVaw3V1Fxrih_hIFcb11PTfsAP)
   6. Create log group for ec2 instance to store logs sent by cloudwatch agent.
   7. Update the `accounts.yaml` file according to your setup done as above.

