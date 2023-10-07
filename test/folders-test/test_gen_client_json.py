from os.path import join,dirname,realpath

from anisynchronise.client_sync import genClientSyncToFile


HERE:str=dirname(realpath(__file__))

genClientSyncToFile(
    vidDir=join(HERE,"test-folders/client/vids"),
    anilogFile=join(HERE,"test-folders/client/client.log"),
    outputFile=join(HERE,"test-folders/workspace/client-sync.json")
)