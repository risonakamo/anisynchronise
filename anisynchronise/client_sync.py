# functions dealing with client sync operation

from os.path import isfile,dirname
from os import listdir,makedirs
from loguru import logger
from json import load
from rich import print as printr

from anisynchronise.anilog import readToSeperator

from anisynchronise.types.ani_log_types import Anilog
from anisynchronise.types.client_sync_types import ClientNodeUpdate

def genClientSyncToFile(
    vidDir:str,
    anilogFile:str,

    outputFile:str
)->None:
    """generate client sync and output to json file. output file name needs extension"""

    printr("[magenta]Generating Client Sync File[/magenta]")
    printr(f"- Videos Dir: [cyan]{vidDir}[/cyan]")
    printr(f"- Anilog File: [cyan]{anilogFile}[/cyan]")
    printr()

    clientSync:ClientNodeUpdate=genClientSyncUpdate(vidDir,anilogFile)

    makedirs(dirname(outputFile),exist_ok=True)

    printr(f"writing client sync to [green]{outputFile}[/green]")
    with open(outputFile,"w") as wfile:
        wfile.write(clientSync.model_dump_json())

def clientSyncFromCollector():
    """perform phase 3 sync, syncing collector's new items into the client.
    checks for existence of "videos-available.txt", and if exists:

    1. mirrors videos from workspace into client vids dir, completely replacing all vids in
    client vids dir
    2. removes videos-available.txt, preventing client sync from collector again
    3. modifies client's anilog file, removing all seperators. adds a new seperator at the top of the
    file"""

    pass


# ---- private ----
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