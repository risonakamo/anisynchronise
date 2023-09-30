# functions dealing with anilog file

from anisynchronise.types.ani_log_types import Anilog, LogItem


def readToSeperator(anilogFile:str)->Anilog:
    """read anilog file, return items only to the first found seperator"""

    with open(anilogFile,"r") as rfile:
        pass

def parseAnilogLine(line:str)->LogItem:
    """parse a single anilog line into log item"""
    pass