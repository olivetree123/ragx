import sys
import logging

import colorlog

# 创建一个控制台处理器

# 在 Python 的 logging 模块中，Handler 和 Logger 可以有各自独立的日志级别。
# 日志记录的级别是由 Logger 和 Handler 的级别共同决定的。
# 具体行为：
# - Logger 的级别决定了消息是否会被传递给任何处理器（Handler）。
# - Handler 的级别决定了消息是否会被实际处理和输出。
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# 创建一个彩色日志格式化器
formatter = colorlog.ColoredFormatter(
    "%(log_color)s%(asctime)s - %(levelname)s [%(name)s] [%(module)s.%(funcName)s:%(lineno)d] %(message)s",
    datefmt="%d/%b/%Y %H:%M:%S",
    reset=True,
    stream=sys.stdout,
    log_colors={
        "DEBUG": "cyan",
        "INFO": "light_black",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red",
    })

# 将格式化器添加到处理器
console_handler.setFormatter(formatter)


def get_logger(name="ragx"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    # 将处理器添加到日志记录器
    logger.addHandler(console_handler)
    return logger
