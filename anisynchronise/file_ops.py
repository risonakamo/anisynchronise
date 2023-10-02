# functions for performing file operations

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
    if result.returncode<=8:
        logger.info("mirror copy success")
        return

    logger.error("robocopy returned error code {}",result.returncode)
    raise Exception("robocopy failed")