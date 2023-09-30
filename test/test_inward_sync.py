from os.path import join,dirname,realpath

from anisynchronise.inward_sync import genClientSyncToFile

HERE:str=dirname(realpath(__file__))

genClientSyncToFile(
    vidDir=r"E:\videos\vids",
    anilogFile=join(HERE,"test-anilog.log"),
    outputFile=join(HERE,"output/update.json")
)