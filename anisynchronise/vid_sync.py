# functions dealing with syncing vid folders

from loguru import logger
from os.path import join
from shutil import move
from rich import print as printr

from anisynchronise.robocopy import mirrorCopy,robomoveFiles

from anisynchronise.types.ani_log_types import Anilog

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

    printr("[green]client sync confirmed[/green]")
    printr()
    printr("[yellow]the following videos will be removed from collector videos dir:[/yellow]")

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
    printr(f"[1/3] removing {len(removeVids)} items from collector vids...")
    for removeVid in removeVids:
        removeVid:str

        logger.debug(f"removing {removeVid}")
        move(
            join(collectorVidsDir,removeVid),
            join(deleteDir,removeVid)
        )


    # 2. moving all items from stockdir into the collector vids dir
    printr("[2/3] moving items from stock dir...")
    robomoveFiles(
        srcdir=stockDir,
        destdir=collectorVidsDir
    )


    # 3. mirroring to workspace dir
    printr("[3/3] mirroring to workspace videos dir...")
    mirrorCopy(
        collectorVidsDir,
        join(workspaceDir,"videos")
    )