'''
Description: 
Version: 
Author: 李瑶瑶
Date: 2021-04-10 17:41:40
LastEditors: 李瑶瑶
LastEditTime: 2021-04-11 13:52:36
'''

import logging

# 编程的方式来写一下高级的语法
# 记录器
logger = logging.getLogger("cn.cccb.applog")
logger.setLevel(logging.DEBUG)

# 处理器handler
consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.DEBUG)

# 没有给handler指定日志级别，将使用logger的级别
fileHander = logging.FileHandler(filename=r"G:\01-python\github\Studyfor\study_logging\addDemo.log")
fileHander.setLevel(logging.INFO)

# formatter格式
formatter1 = logging.Formatter("[%(asctime)s-%(levelname)-8s-%(filename)s-%(lineno)s]%(message)s")
formatter2 = logging.Formatter("[%(asctime)s-%(levelname)-8s-%(filename)s-%(lineno)s]%(message)s")
# %(levelno)s: 打印日志级别的数值
# %(levelname)s: 打印日志级别名称
# %(pathname)s: 打印当前执行程序的路径，其实就是sys.argv[0]
# %(filename)s: 打印当前执行程序名
# %(funcName)s: 打印日志的当前函数
# %(lineno)d: 打印日志的当前行号
# %(asctime)s: 打印日志的时间
# %(thread)d: 打印线程ID
# %(threadName)s: 打印线程名称
# %(process)d: 打印进程ID
# %(message)s: 打印日志信息

# 给处理器设置格式
consoleHandler.setFormatter(formatter1)
fileHander.setFormatter(formatter2)

# 记录器要设置处理器
logger.addHandler(consoleHandler)
logger.addHandler(fileHander)

# 定义一个过滤器
flt = logging.Filter("cn.cccb")

# 关联过滤器
# logger.addFilter(flt)
# 也可以单独关联过滤器
fileHander.addFilter(flt)

# 打印日志的代码
logger.info("info")
logger.debug("debug")

# 异常信息
a = "abc"
try:
    int(a)
except Exception as e:
    logger.exception(e)

