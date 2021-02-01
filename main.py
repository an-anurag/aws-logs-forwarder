# -*- coding: utf-8 -*-
"""A main logic to continuously running this script"""

import time
import socket
from threading import Thread

from bundle.cloudwatch_forwarder import CloudWatchForwarder
from bundle.logger import logger
from bundle.config_reader import conf
from bundle.yaml_reader import get_confs

HOST = conf.read('syslog', 'host')
PORT = conf.read('syslog', 'port')


def main():
    """
    A main logic
    """

    try:
        # get conf from yaml file
        accounts = get_confs()['accounts']

        # for each account in yaml
        for acc in accounts:
            acc_id = acc['id']
            acc_profile = acc['profile']
            log_group = acc['log_groups'][0]

            # initialize cloudwatch object
            cloudwatch = CloudWatchForwarder(
                user_profile=acc_profile,
                acc_id=acc_id,
                log_group=log_group,
                host=HOST,
                port=PORT,
            )
            # one thread for each cloudwatch object
            thread = Thread(target=cloudwatch.run)
            thread.start()

    except socket.timeout as err:
        logger.exception("timeout occurred, trying again", err)
        time.sleep(60)
        return main()
    except socket.gaierror as err:
        logger.exception("Connection error, trying again", err)
        time.sleep(60)
        return main()
    except IOError as err:
        logger.exception('No storage space left on sensor')
    except Exception as err:
        logger.exception(err)


if __name__ == '__main__':
    main()
