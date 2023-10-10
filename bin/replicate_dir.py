# tool for creating test folders

from argparse import ArgumentParser
from devtools import debug

from pydantic import BaseModel

from anisynchronise.testing import replicateDir

class Args(BaseModel):
    src:str
    dest:str

def getArgs()->Args:
    """get args from arg parse"""

    parser:ArgumentParser=ArgumentParser(
        description="""mock replicate target directory. output directory will have all
        the same filenames, but the files will just be text files"""
    )

    parser.add_argument("src",help="src folder")
    parser.add_argument("dest",help="dest folder")

    return Args.model_validate(vars(parser.parse_args()))

if __name__=="__main__":
    args:Args=getArgs()

    replicateDir(
        src=args.src,
        dest=args.dest
    )