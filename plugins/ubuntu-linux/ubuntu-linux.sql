
DELETE from plugin where id = 4569;

DELETE from plugin_sid where plugin_id = 4569;

INSERT ignore INTO plugin(id,type,name,description,vendor,product_type) values(4569,1,'AWS-Console','A Cloud Service','Amazon',20);

INSERT IGNORE INTO plugin_sid (plugin_id, sid, category_id, subcategory_id, class_id, priority, reliability, name) VALUES


(4569,1,1,1,NULL,2,2, 'AWS-EC2-AMI: A user has been created in EC2 instance AMI'),
(4569,2,1,1,NULL,2,2, 'AWS-EC2-AMI: A user has been deleted from EC2 instance AMI'),
(4569,3,1,1,NULL,2,2, 'AWS-EC2-AMI: An unattended upgrade has been performed in EC2 AMI'),
(4569,4,1,1,NULL,2,2, 'AWS-EC2-AMI: A package installed in EC2 AMI by user');
