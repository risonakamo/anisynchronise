from os import listdir
from devtools import debug
from os.path import dirname,realpath,join

from anisynchronise.vid_sync import checkCollectorSync
from anisynchronise.client_sync import clientSyncToRemoveVids, readClientSync

from anisynchronise.types.client_sync_types import ClientNodeUpdate

HERE:str=dirname(realpath(__file__))

collectorVidsDir:str=r"E:\videos\vids"
collectorVids:list[str]=listdir(collectorVidsDir)
debug(collectorVids)

clientSync:ClientNodeUpdate=readClientSync(join(HERE,"test-update.json"))
debug(clientSync)

res:bool=checkCollectorSync(
    collectorVids=collectorVids,
    removeVids=clientSyncToRemoveVids(clientSync),
    clientVids=clientSync.vidState
)

print(res)