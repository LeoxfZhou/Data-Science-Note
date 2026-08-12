import logging
import os


def configure_logger(name: str) -> logging.Logger:
    """创建结构一致的日志器，避免各服务重复添加处理器。"""
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    level = os.getenv("SMARTGATE_LOG_LEVEL", "INFO").upper()
    logger.setLevel(level)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s"))
    logger.addHandler(handler)
    return logger
