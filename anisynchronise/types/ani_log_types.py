# typings for ani logger log

from typing import TypeAlias
from pydantic import BaseModel

class LogItem(BaseModel):
    """an entry from the log"""

    filename:str
    date:str

Anilog:TypeAlias=list[LogItem]
"""anilog object is just list of log items. sorted by latest to oldest"""