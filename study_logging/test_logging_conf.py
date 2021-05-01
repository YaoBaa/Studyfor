'''
Description: 
Version: 
Author: 李瑶瑶
Date: 2021-04-11 17:51:26
LastEditors: 李瑶瑶
LastEditTime: 2021-04-11 18:15:06
'''

import logging
import logging.config

CONF_LOG = r"G:\01-python\github\Studyfor\study_logging\logging.conf"
logging.config.fileConfig(CONF_LOG)

logger1 = logging.getLogger("1")
logger2 = logging.getLogger("2")

logger1.info("logger1: it is a info message")
logger1.debug("logger1: it is a debug message")
logger2.info("logger1: it is a info message")
logger2.debug("logger1: it is a debug message")
