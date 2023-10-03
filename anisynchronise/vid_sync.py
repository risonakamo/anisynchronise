# functions dealing with syncing vid folders

from loguru import logger

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

    return True