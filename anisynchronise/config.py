from yaml import safe_load


from pydantic import BaseModel
from typing import Literal, TypeAlias

SystemType:TypeAlias=Literal["client","collector"]
"""what the system should be considered as"""

class AnisyncConfig(BaseModel):
    vidsDir:str
    anilogFile:str

    syncDir:str
    """remote directory used as workspace for inter-system operations. should probably be
    in an external drive"""

    systemType:SystemType

def loadConfig(path:str)->AnisyncConfig:
    """load anisync config"""

    with open(path,"r") as rfile:
        return AnisyncConfig.model_validate(safe_load(rfile))