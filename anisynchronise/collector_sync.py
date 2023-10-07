# top level of collector sync. contains main function for doing collector sync

from os import listdir
from os.path import join
from loguru import logger

from anisynchronise.anilog import addToLog, anilogAsFilenames
from anisynchronise.client_sync import readClientSync
from anisynchronise.vid_sync import checkCollectorSync, doCollectorVidSync

from anisynchronise.types.client_sync_types import ClientNodeUpdate


def doCollectorSync(
    collectorVidsDir:str,
    stockDir:str,
    deleteDir:str,
    workspaceDir:str,

    collectorAnilogFile:str,
    clientSyncJson:str
)->None:
    """collector sync. see collector-sync.md for info about collector sync operation.
    requires all the items specified by the docs"""

    # 1. reading from client sync json
    logger.info("reading from client sync json")
    clientsync:ClientNodeUpdate=readClientSync(clientSyncJson)

    collectorVidsList:list[str]=listdir(collectorVidsDir)

    removeVidsList:list[str]=anilogAsFilenames(clientsync.logUpdate)

    logger.info("confirming collector sync operation correctness")
    if not checkCollectorSync(
        collectorVids=collectorVidsList,
        removeVids=removeVidsList,
        clientVids=clientsync.vidState
    ):
        logger.error("failed collector sync check")
        raise Exception("failed collector sync check")

    # 2.,3.,4. do video sync
    logger.info("performing collector sync")
    doCollectorVidSync(
        collectorVidsDir=collectorVidsDir,
        stockDir=stockDir,
        deleteDir=deleteDir,
        workspaceDir=workspaceDir,

        removeVids=removeVidsList
    )

    # 5. update collector anilog file
    logger.info("updating collector anilog")
    addToLog(
        anilogFile=collectorAnilogFile,
        items=clientsync.logUpdate,
    )

    # 6. create drop ready file
    with open(join(workspaceDir,"videos-available.txt"),"w"):
        pass

    logger.info("collector sync successful")