-- plugin_id = 115005
-- type = detector


DELETE from plugin where id = 115005;
DELETE from plugin_sid where plugin_id=115005;

INSERT ignore INTO plugin(id,type,name,description,vendor,product_type) values(115005,1,'centos','an open source os','redhat',20);

INSERT IGNORE INTO plugin_sid (plugin_id, sid, category_id, subcategory_id, class_id, priority, reliability, name) VALUES

(115005,101,1,1,NULL,2,2, 'CentOS-Audit - Indirect system call to kernel success'),
(115005,102,1,1,NULL,2,2, 'CentOS-Audit - Indirect system call to kernel failure'),
(115005,103,1,1,NULL,2,2, 'CentOS-Audit - Current working directory recorded'),
(115005,104,1,1,NULL,2,2, 'CentOS-Audit - File name path information recorded'),
(115005,105,1,1,NULL,2,2, 'CentOS-Audit - Full command line has given to the process'),

(115005,201,1,1,NULL,2,2, 'CentOS-YUM - Package installed'),
(115005,202,1,1,NULL,2,2, 'CentOS-YUM - Package updated'),

(115005,301,1,1,NULL,2,2, 'CentOS-Mail - Mail sent'),
(115005,302,1,1,NULL,2,2, 'CentOS-Mail - Mail received'),
(115005,303,1,1,NULL,2,2, 'CentOS-Mail - Starting postfix system'),
(115005,304,1,1,NULL,2,2, 'CentOS-Mail - Stopping postfix system'),

(115005,401,1,1,NULL,2,2, 'CentOS-Message - System activity message'),

(115005,501,1,1,NULL,2,2, 'CentOS-Secure - Connection closed'),
(115005,502,1,1,NULL,2,2, 'CentOS-Secure - Session closed'),
(115005,503,1,1,NULL,2,2, 'CentOS-Secure - Accepted Keyboard'),
(115005,504,1,1,NULL,2,2, 'CentOS-Secure - Session opened'),

(115005,601,1,1,NULL,2,2, 'CentOS-Cron - Session closed'),
(115005,602,1,1,NULL,2,2, 'CentOS-Cron - Accepted Keyboard'),

(115005,701,1,1,NULL,2,2, 'CentOS-HTTP - HTTP Access'),
(115005,702,1,1,NULL,2,2, 'CentOS-HTTP - HTTP dummy host access'),
(115005,703,1,1,NULL,2,2, 'CentOS-HTTP - HTTP server error'),

(115005,801,1,1,NULL,2,2, 'CentOS-mysql: Mysql daemon starting'),
(115005,802,1,1,NULL,2,2, 'CentOS-mysql: Mysql normal shutdown'),
(115005,803,1,1,NULL,2,2, 'CentOS-mysql: Mysql abnormal shutdown'),
(115005,804,1,1,NULL,2,2, 'CentOS-mysql: Mysql ready for connections'),

(115005,901,1,1,NULL,2,2, 'CentOS-boot: Host boot started'),

(115005,1001,1,1,NULL,2,2, 'CentOS-kernel: kernel alert'),

(115005,1101,1,1,NULL,2,2, 'CentOS-auth: session opened for the user'),
(115005,1102,1,1,NULL,2,2, 'CentOS-auth: session closed for the user');