# typings used during inward sync process

from pydantic import BaseModel
from anisynchronise.types.ani_log_types import LogItem

class ClientNodeUpdate(BaseModel):
    """sync state from a client node to be sent to collector node. includes information
    about the client node"""

    logUpdate:list[LogItem]
    """all log updates from the client from the last seperator"""

    vidState:list[str]
    """all files in the vid folder of the client"""