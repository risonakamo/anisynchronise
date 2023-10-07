from os.path import dirname,join,realpath
from os import chdir
from subprocess import run

HERE:str=dirname(realpath(__file__))

chdir(HERE)

run(
    "regen-test-folder.bat",
    shell=True
)

run(
    "python test_gen_client_json.py",
    shell=True,
    check=True
)

run(
    "python test_collector_sync.py",
    shell=True,
    check=True
)