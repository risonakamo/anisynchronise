from pydantic import BaseModel
from typing import TypeAlias,Literal

SystemType:TypeAlias=Literal["client","collector"]
"""what the system should be considered as"""

class CollectorConfig(BaseModel):
    """yaml configuration for collector"""

    systemType:Literal["collector"]

    collectorVideosDir:str
    stockVideosDir:str
    videosDeleteDir:str

    workspaceDir:str

    collectorAnilogFile:str

class ClientConfig(BaseModel):
    """yaml configuration for client"""

    systemType:Literal["client"]

    clientVideosDir:str
    videosDeleteDir:str

    workspaceDir:str

    clientAnilogFile:str