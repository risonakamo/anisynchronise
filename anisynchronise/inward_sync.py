# functions dealing with inward sync operation

from os.path import isfile
from os import listdir
from loguru import logger

from anisynchronise.anilog import readToSeperator

from anisynchronise.types.ani_log_types import Anilog
from anisynchronise.types.inward_sync_types import ClientNodeUpdate


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

    logger.info("writing client sync to {}",outputFile)
    with open(outputFile,"w") as wfile:
        wfile.write(clientSync.model_dump_json())