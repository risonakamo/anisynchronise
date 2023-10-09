# functions dealing with testing

from os import listdir, makedirs
from os.path import join, isfile

from loguru import logger

def replicateDir(src:str,dest:str)->None:
    """copy a dir, but all the files in the dir are just single text files. the name of the files are
    the same as in the src. only does 1 level (no recursion)"""

    srcItems:list[str]=listdir(src)

    makedirs(dest,exist_ok=True)

    for item in srcItems:
        item:str

        itemPath:str=join(src,item)

        if not isfile(itemPath):
            logger.info("?")
            continue

        logger.info("replicating {}",item)

        with open(join(dest,item),"w") as wfile:
            wfile.write(item)
