# functions dealing with anilog file

from re import Match, match,search
from loguru import logger
from rich import print as printr

from anisynchronise.types.ani_log_types import Anilog, LogItem


def readToSeperator(anilogFile:str)->Anilog:
    """read anilog file, return items only to the first found seperator"""

    return readAnilog(anilogFile,True)

def addToLog(
    anilogFile:str,
    items:Anilog,
    output:str|None=None
)->None:
    """append the given items to the start of the anilog. give output to specify new output file, or none
    to overwrite"""

    anilog:Anilog=readAnilog(anilogFile)

    printr(f"adding {len(items)} items to log")

    anilog=items+anilog

    if not output:
        output=anilogFile

    writeAnilog(anilog,output)

def anilogAsFilenames(anilog:Anilog)->list[str]:
    """convert anilog into simple list of file names of items in the log"""

    return [
        item.filename
        for item in anilog
    ]




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

def logItemToText(item:LogItem)->str:
    """convert log item to text"""

    return f"{item.date} {item.filename}"

def writeAnilog(anilog:Anilog,outputFile:str)->None:
    """write given anilog to target file. filename needs extension"""

    text:str=""

    for item in anilog:
        item:LogItem

        text+=logItemToText(item)+"\n"

    printr(f"writing to anilog: [green]{outputFile}[/green]")
    with open(outputFile,"w") as wfile:
        wfile.write(text)

def readAnilog(anilogFile:str,stopAtSeperator:bool=False)->Anilog:
    """read anilog file"""

    log:Anilog=[]

    with open(anilogFile,"r") as rfile:
        while True:
            line:str=rfile.readline()

            if stopAtSeperator and matchSeperator(line):
                logger.debug("finish reading anilog to seperator: {} items",len(log))
                return log

            if not line:
                logger.debug("read whole anilog file")
                return log

            log.append(parseAnilogLine(line))