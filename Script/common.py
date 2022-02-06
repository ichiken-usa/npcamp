import os
import json
from logging import getLogger

import log

### Log ###
LOG_DIR = './Script/Log/'
logger = getLogger(__name__)
log.set_log_config(logger, LOG_DIR, 'common.log')


def read_json_from_current_folder(filename):

    try:
        dir = os.path.join(os.path.dirname(__file__), filename)
        with open(dir, mode="r") as f:
            json_obj = json.load(f)

        logger.debug(json_obj)

        return json_obj

    except Exception as e:
        logger.exception(e)