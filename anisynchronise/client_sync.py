# functions dealing with client sync operation

from os.path import isfile,dirname
from os import listdir,makedirs
from loguru import logger
from json import load

from anisynchronise.anilog import readToSeperator

from anisynchronise.types.ani_log_types import Anilog
from anisynchronise.types.client_sync_types import ClientNodeUpdate


def genClientSyncUpdate(
    vidDir:str,
    anilogFile:str
)->ClientNodeUpdate:
    """generate client node update from client node's target folders"""

    vidFiles:list[str]=listdir(vidDir)

    anilogUpdate:Anilog=readToSeperator(anilogFile)

    return ClientNodeUpdate(
        vidState=vidFiles,
        logUpdate=anilogUpdate
    )

def genClientSyncToFile(
    vidDir:str,
    anilogFile:str,

    outputFile:str
)->None:
    """generate client sync and output to json file. output file name needs extension"""

    clientSync:ClientNodeUpdate=genClientSyncUpdate(vidDir,anilogFile)

    makedirs(dirname(outputFile),exist_ok=True)

    logger.info("writing client sync to {}",outputFile)
    with open(outputFile,"w") as wfile:
        wfile.write(clientSync.model_dump_json())

def readClientSync(file:str)->ClientNodeUpdate:
    """read client sync json file"""

    with open(file,"r") as rfile:
        return ClientNodeUpdate.model_validate(load(rfile))

def clientSyncToRemoveVids(clientSync:ClientNodeUpdate)->list[str]:
    """convert client sync to list of files to be removed. this list is just the list of
    items in the log update"""

    return [
        item.filename
        for item in clientSync.logUpdate
    ]