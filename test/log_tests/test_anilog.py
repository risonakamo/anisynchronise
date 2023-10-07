# test anilog functions

from os.path import join,dirname,realpath
from devtools import debug

from anisynchronise.anilog import addToLog, readToSeperator
from anisynchronise.types.ani_log_types import Anilog

HERE:str=dirname(realpath(__file__))

def test_readToSeperator():
    """test reading to seperator

    success: should see a number of items printed out from the log"""

    log:Anilog=readToSeperator(join(HERE,"log1.log"))
    debug(log)

def test_writeToLog():
    """test reading to sepereator, and adding the read items to a 2nd log

    success: should see entries up to the sepereator in log1 added to log2"""

    logupdate:Anilog=readToSeperator(join(HERE,"log1.log"))
    addToLog(join(HERE,"log2.log"),logupdate)

if __name__=="__main__":
    # test_readToSeperator()
    test_writeToLog()
