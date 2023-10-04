# functions for performing robocopy operations

from subprocess import CompletedProcess, run

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

def roboMove(src:str,dest:str)->None:
    """move target location to another. merges dest folders if folder already exists"""

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

def robocopySuccess(returnCode:int)->bool:
    """return if code is good robocopy return code"""

    return returnCode<=8