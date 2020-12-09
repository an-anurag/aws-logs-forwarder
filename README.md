LTS - AWS INTEGRATION DEPLOYMENT
----------------------------------------

* PREREQUISITES
------------------------------------------------
   1. Sign up for AWS account
   2. Go to `IAM` and create a IAM user with existing policy `CloudWatchEventsFullAccess`, download the credential file at the last step of user creation. [see creating IAM user](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwi2--bFhZvqAhVC4XMBHUP2CwwQFjAAegQIBBAB&url=https%3A%2F%2Fdocs.aws.amazon.com%2FIAM%2Flatest%2FUserGuide%2Fid_users_create.html&usg=AOvVaw1QBSa1KvEcA6W3pn9hJfzn)
   3. Install the `AWS cli` on a host (linux) where you want to deploy the code.
   4. Enter the `aws configure` on the terminal
   5. Enter all the details at prompt such as access key and secret key from credential file downloaded earlier.
   2. Go to `CloudWatch` in web management console and create a `log-group` and `streams` for each log source. [see creating log group](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwilt6qvhZvqAhXlyzgGHRVsDvcQFjABegQIDBAD&url=https%3A%2F%2Fdocs.aws.amazon.com%2FAmazonCloudWatch%2Flatest%2Flogs%2FWorking-with-log-groups-and-streams.html%23%3A~%3Atext%3DTo%2520create%2520a%2520log%2520group%2Cthen%2520choose%2520Create%2520log%2520group.&usg=AOvVaw2lL2qcHRVtpOur6tSUV8Qp)
   3. Go to CloudTrail and create a trail, [see creating trail](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwi16NTxhJvqAhWd93MBHdpnBK0QFjABegQIDRAD&url=https%3A%2F%2Fdocs.aws.amazon.com%2Fawscloudtrail%2Flatest%2Fuserguide%2Fcloudtrail-create-a-trail-using-the-console-first-time.html%23%3A~%3Atext%3DTo%2520create%2520a%2520CloudTrail%2520trail%2520with%2520the%2520AWS%2520Management%2520Console%26text%3DChoose%2520the%2520AWS%2520Region%2520where%2CChoose%2520Get%2520Started%2520Now.%26text%3DIf%2520you%2520do%2520not%2520see%2Ca%2520name%2520for%2520your%2520trail.&usg=AOvVaw1uvcfOEFwcgGR2ZNTDMBTB)
   4. Configure trail with log-group to send logs to.
   5. If you want to monitor EC2 instance, then install CloudWatch agent in every instance and configure it. [see install CW-agent](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwib9sOFhpvqAhWXbn0KHexhACQQFjAAegQIAhAB&url=https%3A%2F%2Fdocs.aws.amazon.com%2FAmazonCloudWatch%2Flatest%2Fmonitoring%2Finstall-CloudWatch-Agent-on-EC2-Instance.html&usg=AOvVaw3V1Fxrih_hIFcb11PTfsAP)


* DEPLOYMENT
--------------------------------------------------

1. CODE

    1. Get the code from SVN.
    2. AWS plugin is at SVN --> SIEM --> Addons --> log_generators --> aws_console .
    3. Configure the `setup.cfg` in aws_console directory with below details
    4. Add CloudWatch `log-group` name, `stream` names and logger input details.
    3. Run the main.py file with `python3 main.py` in background and must not be terminated.

2. LOGGER
    1. AWS logs will get collected in logger inputs added in `cfg` file.
    2. Create output in logger with host being the IP address you want to forward AWS logs to.
    3. Create stream in logger.
    4. Assign output to the stream and AWS log forwarding will get started to the host specified in output.
    
3. HOST: (Sensor/SIEM)

  * If Sensor is the log receiver

       1. Login to the host SENSOR.
       2. Make sure logs are coming in  `/var/log/alienvault/devices/<ip-address>/<ip-address.log>`.
       3. Above file will contain real time AWS logs coming from the logger.
       4. Create `aws.conf` file in `/etc/rsyslog.d/` and add line if `$rawmsg contains 'AWS-Console' then /var/log/aws-console.log` in it. 
       5. This will append AWS logs in `/var/log/aws-console.log` file contineously.
       6. Place `aws-console.cfg` file at `/etc/ossim/agent/plugins/`
       7. Place `aws-console.sql` file at `/usr/share/doc/ossim-mysql/contrib/plugins/` in SIEM only.
       8. Enter `cat /usr/share/doc/ossim-mysql/contrib/plugins/aws-console.sql | ossim-db` command.
       9. Goto OSSIM console by using `ossim-setup` command and enable the `aws-console.cfg` plugin.
       10. Enter the `ossim-reconfig` command.
       11. You can see the AWS events at `SIEM --> Events --> Security Events --> Datasource --> AWS-Console` in real time.
  
  * If SIEM is the log receiver

       1. Login to the host SIEM.
       2. Make sure logs are coming in  `/var/log/alienvault/devices/<ip-address>/<ip-address.log>`.
       3. Above file will contain real time AWS logs coming from the logger.
       4. Create `aws.conf` file in `/etc/rsyslog.d/` and add line if `$rawmsg contains 'AWS-Console' then /var/log/aws-console.log` in it. 
       5. This will append AWS logs in `/var/log/aws-console.log` file contineously.
       6. Place `aws-console.cfg` and `aws-console.sql` in appropriate locations (`/etc/ossim/agent/plugins/` and `/usr/share/doc/ossim-mysql/contrib/plugins/` respectively.)
       8. Enter `cat /usr/share/doc/ossim-mysql/contrib/plugins/aws-console.sql | ossim-db` command.
       9. Goto OSSIM console by using `ossim-setup` command and enable the `aws-console.cfg` plugin.
       10. Enter the `ossim-reconfig` command.
       11. You can see the AWS events at `SIEM --> Events --> Security Events --> Datasource --> AWS-Console` in real time.

1. Note
    1. Note that sql file can only be placed at SIEM and not at sensor.