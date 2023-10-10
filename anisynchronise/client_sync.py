# functions dealing with client sync operation

from os.path import isfile,dirname,join,isdir
from os import listdir,makedirs, remove
from loguru import logger
from json import load
from rich import print as printr

from anisynchronise.anilog import readToSeperator, resetSeperator
from anisynchronise.robocopy import mirrorCopy

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

def clientSyncFromCollector(
    workspaceDir:str,
    videosDir:str,
    anilogFile:str
)->None:
    """perform phase 3 sync, syncing collector's new items into the client.
    only works if videos-available.txt exists in the workspace dir

    see client-sync.md, phase 3 client sync for operations performed"""

    printr("[magenta]Client Sync Phase 3[/magenta]")

    # confirming videos are available
    videosAvailFile:str=join(workspaceDir,"videos-available.txt")
    if not isfile(videosAvailFile):
        printr(
            "[bold red]ERROR: Could not find videos-available.txt "
            +"in workspace dir, refusing to do phase 3 sync[/bold red]"
        )
        raise Exception("missing videos available")

    # 1. mirroring workspace videos into client vids dir
    printr("mirroring into videos dir...")
    workspaceVidsDir:str=join(workspaceDir,"videos")

    if not isdir(workspaceVidsDir):
        printr("[bold red]ERROR: Missing workspace vids dir[/bold red]")
        raise Exception("missing workspace vids dir")

    mirrorCopy(
        src=workspaceVidsDir,
        dest=videosDir
    )

    # 2. edit anilog file to remove all seperators and replace one at the top
    printr("resetting anilog file seperators...")
    resetSeperator(anilogFile)

    # 3. delete the videos available file
    printr("deleting videos-available.txt")
    remove(videosAvailFile)

    printr("[green]client sync phase 3 complete[/green]")


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