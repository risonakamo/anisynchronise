# functions dealing with anilog file

from re import Match, match,search
from loguru import logger

from anisynchronise.types.ani_log_types import Anilog, LogItem


def readToSeperator(anilogFile:str)->Anilog:
    """read anilog file, return items only to the first found seperator"""

    log:Anilog=[]

    with open(anilogFile,"r") as rfile:
        while True:
            line:str=rfile.readline()

            if matchSeperator(line):
                logger.info("finish reading anilog to seperator: {} items",len(log))
                return log

            if not line:
                logger.warning("reached end of anilog file without finding seperator")
                return log

            log.append(parseAnilogLine(line))





# ---- PRIVATE ----
def parseAnilogLine(line:str)->LogItem:
    """parse a single anilog line into log item"""

    # [0]: text
    # [1]: date
    # [2]: file name
    res:Match|None=match(
        r"(\d+-\d+-\d+ \d+:\d+:\d+) (.*)",
        line
    )

    if not res or len(res.groups())!=2:
        logger.error("failed to parse anilog line")
        logger.error("error line: {}",line)
        raise Exception("failed anilog line parse")

    return LogItem(
        filename=res[2],
        date=res[1]
    )

def matchSeperator(text:str)->bool:
    """check if given line of text matches seperator"""

    # regex true if text has 3 dashes in a row anywhere in it
    return bool(search("---",text))