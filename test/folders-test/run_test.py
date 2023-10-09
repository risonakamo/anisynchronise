from os.path import dirname,join,realpath
from os import chdir
from subprocess import run
from loguru import logger
from sys import stdout

from anisynchronise.collector_sync import doCollectorSync
from anisynchronise.client_sync import genClientSyncToFile

HERE:str=dirname(realpath(__file__))

logger.remove()
logger.add(stdout,level="INFO")

chdir(HERE)

run(
    "regen-test-folder.bat",
    shell=True,
    capture_output=True
)

logger.info("client sync test")
genClientSyncToFile(
    vidDir=join(HERE,"test-folders/client/vids"),
    anilogFile=join(HERE,"test-folders/client/client.log"),
    outputFile=join(HERE,"test-folders/workspace/client-sync.json")
)

print()
print()
print()
print()
print()
logger.info("collector sync test")
doCollectorSync(
    collectorVidsDir=join(HERE,"test-folders/collector/vids"),
    stockDir=join(HERE,"test-folders/collector/stock"),
    deleteDir=join(HERE,"test-folders/collector/delete"),
    workspaceDir=join(HERE,"test-folders/workspace"),
    collectorAnilogFile=join(HERE,"test-folders/collector/collector.log"),
    clientSyncJson=join(HERE,"test-folders/workspace/client-sync.json")
)