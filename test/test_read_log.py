# tests reading log to seperator. succeeds if file completes

from os.path import join,dirname,realpath
from devtools import debug

from anisynchronise.anilog import readToSeperator
from anisynchronise.types.ani_log_types import Anilog

HERE:str=dirname(realpath(__file__))

log:Anilog=readToSeperator(join(HERE,"test-anilog.log"))
debug(log)