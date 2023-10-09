#  functions for loading config files

from loguru import logger
from yaml import safe_load

from anisynchronise.types.config_types import ClientConfig, CollectorConfig


def loadConfig(path:str)->CollectorConfig|ClientConfig:
    """load config. can be collector or client"""

    with open(path,"r") as rfile:
        data=safe_load(rfile)

        if data["systemType"]=="collector":
            return CollectorConfig.model_validate(data)

        elif data["systemType"]=="client":
            return ClientConfig.model_validate(data)

        else:
            logger.error("failed to parse config")
            raise Exception("unknown config")