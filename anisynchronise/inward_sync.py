# functions dealing with inward sync operation

from os.path import isfile
from os import listdir

from anisynchronise.types.inward_sync_types import ClientNodeUpdate


def genClientSyncUpdate(
    vidDir:str,
    anilogFile:str
)->ClientNodeUpdate:
    """generate client node update from client node's target folders"""

    vidFiles:list[str]=listdir(vidDir)

