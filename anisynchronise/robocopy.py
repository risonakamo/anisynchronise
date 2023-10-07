# functions for performing robocopy operations

from os import listdir
from os.path import join,isdir
from subprocess import CompletedProcess, run
from devtools import debug
from typing_extensions import deprecated

from loguru import logger


def mirrorCopy(src:str,dest:str)->None:
    """mirror copy the src to the dest. the dest will be completely overwritten by the src"""

    logger.info("mirror copying")
    result:CompletedProcess=run(
        [
            "robocopy",
            "/mir",
            src,
            dest
        ],
        shell=True
    )

    # error less than 8 is sucess for robocopy for some reason...
    if robocopySuccess(result.returncode):
        logger.info("mirror copy success")
        return

    logger.error("robocopy returned error code {}",result.returncode)
    raise Exception("robocopy failed")

def robomoveFiles(
    srcdir:str,
    destdir:str,
    files:list[str]
)->None:
    """move target files, which all must be in the src dir, to another dir. leaves the
    src dir completely empty"""

    logger.info("robomoving files")
    result:CompletedProcess=run(
        [
            "robocopy",
            "/move",
            srcdir,
            destdir,
            *files
        ]
    )

    if not robocopySuccess(result.returncode):
        logger.error("failed to robomove files")
        raise Exception("robomove failed")

    logger.info("clearing src dir")
    run(
        [
            "del",
            "/q",
            join(srcdir,"*.*")
        ],
        shell=True,
        check=True
    )




# --- private ---
@deprecated("replaced by robomove files")
def dep_roboMove(src:str,dest:str)->None:
    """move target location to another. if used on directories, removes the original directory"""

    logger.info("robo moving")
    result:CompletedProcess=run(
        [
            "robocopy",
            "/move",
            src,
            dest
        ],
        shell=True
    )

    if robocopySuccess(result.returncode):
        logger.info("robo move success")
        return

    logger.error("robocopy failed to do move")
    raise Exception("robocopy move failed")

@deprecated("replaced by robomove files")
def dep_roboMoveInsideDir(src:str,dest:str)->None:
    """move all items inside of src to dest using robomove. used to move all items inside of a dir
    without deleting the dir (which normal robomove would do)"""

    if not isdir(src):
        logger.error("robomove failed, src was not a dir")
        raise Exception("bad src")

    if not isdir(dest):
        logger.error("robomove failed, dest was not a dir")
        raise Exception("bad dest")

    items:list[str]=listdir(src)

    for item in items:
        item:str

        dep_roboMove(
            join(src,item),
            join(dest,item)
        )

def robocopySuccess(returnCode:int)->bool:
    """return if code is good robocopy return code"""

    return returnCode<=8