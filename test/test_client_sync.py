from os.path import join,dirname,realpath
from pytest import mark

from anisynchronise.client_sync import genClientSyncToFile

HERE:str=dirname(realpath(__file__))

@mark.skip()
def test_syncToFile():
    """test generating update.json sync file"""

    genClientSyncToFile(
        vidDir=r"E:\videos\vids",
        anilogFile=join(HERE,"test-anilog.log"),
        outputFile=join(HERE,"output/update.json")
    )