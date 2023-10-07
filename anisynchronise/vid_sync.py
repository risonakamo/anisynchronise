# functions dealing with syncing vid folders

from loguru import logger
from os.path import join
from shutil import move
from anisynchronise.robocopy import mirrorCopy,robomoveFiles

from anisynchronise.types.ani_log_types import Anilog

printr=print

def checkCollectorSync(
    collectorVids:list[str],
    removeVids:list[str],
    clientVids:list[str]
)->bool:
    """given list of collector's vids, list of vids to be removed from collector vids, and the list
    of client vids, check if the sync operation would be successful. warn on anything that would be
    an issue.

    in order to be successful, the collector vids minus the remove vids must equal the client
    vids. if there are any missing remove vids, display the missing vids. if there are
    any extra vids in client vids after removals, mention the extra client vids

    any missing vids from client is ok (client does not have something that is in collector vids.
    but the client must not have any vids that the collector does not (client must be subset after
    removal operation)"""

    collectorVidsSet:set[str]=set(collectorVids)
    removeVidsSet:set[str]=set(removeVids)
    clientvidsSet:set[str]=set(clientVids)

    # find items in remove set that is missing in collector set
    missingCollectorVids:set[str]=removeVidsSet-collectorVidsSet

    if len(missingCollectorVids):
        logger.error("attempted to remove videos, but missing videos from collector dir")
        print("missing the following files:")

        for missingvid in missingCollectorVids:
            missingvid:str

            printr(f"- {missingvid}")

        return False

    # check for vids the client has that the collector doesn't have
    missingCollectorVids2:set[str]=clientvidsSet-collectorVidsSet

    if len(missingCollectorVids2):
        logger.error("client has vids that collector does not")
        print("client has the following extra files:")

        for missingvid in missingCollectorVids2:
            missingvid:str

            printr(f"- {missingvid}")

        return False

    logger.info("client sync confirmed")
    logger.info("the following videos will be removed:")

    for vid in removeVids:
        printr(f"- {vid}")

    return True

def doCollectorVidSync(
    collectorVidsDir:str,
    stockDir:str,
    deleteDir:str,
    workspaceDir:str,

    removeVids:list[str]
)->None:
    """do vids sync portion of collector sync

    removeVids should be list of filenames only

    1. removes specified remove vids from collector vids dir, moving them into the deleteDir
    2. moves all vids from stock to collector vids dir. empties the stock dir
    3. mirrors all collector vids to workspace dir vids, replacing whatever was there originally"""

    # 1. removing all removeVids from collector vids
    logger.info("removing items from collector vids...")
    for removeVid in removeVids:
        removeVid:str

        printr(f"removing {removeVid}")
        move(
            join(collectorVidsDir,removeVid),
            join(deleteDir,removeVid)
        )


    # 2. moving all items from stockdir into the collector vids dir
    logger.info("moving items from stock dir...")
    robomoveFiles(
        srcdir=stockDir,
        destdir=collectorVidsDir
    )


    # 3. mirroring to workspace dir
    logger.info("mirroring to workspace videos dir")
    mirrorCopy(
        collectorVidsDir,
        join(workspaceDir,"videos")
    )