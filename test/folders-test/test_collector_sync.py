from os.path import join,dirname,realpath

from anisynchronise.collector_sync import doCollectorSync


HERE:str=dirname(realpath(__file__))

doCollectorSync(
    collectorVidsDir=join(HERE,"test-folders/collector/vids"),
    stockDir=join(HERE,"test-folders/collector/stock"),
    deleteDir=join(HERE,"test-folders/collector/delete"),
    workspaceDir=join(HERE,"test-folders/workspace"),
    collectorAnilogFile=join(HERE,"test-folders/collector/collector.log"),
    clientSyncJson=join(HERE,"test-folders/workspace/client-sync.json")
)