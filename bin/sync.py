# main sync program. reads config to determine what type of computer to choose sync task

from os import makedirs
from os.path import dirname,realpath,join,isdir,isfile
from rich import print as printr

from anisynchronise.config import loadConfig
from anisynchronise.types.config_types import ClientConfig, CollectorConfig

HERE:str=dirname(realpath(__file__))

config:CollectorConfig|ClientConfig=loadConfig(join(HERE,"../config/config.yml"))

if config.systemType=="collector":
    printr("[magenta]--- System Type: [cyan]Collector[/cyan] ---[/magenta]")

    printr("[yellow]Checking for Client Sync Json...[/yellow]")
    clientSyncJsonPath:str=join(config.workspaceDir,"client-sync.json")
    if not isfile(clientSyncJsonPath):
        printr(
            f"[bold red]ERROR: Could not find client sync json at: "
            +f"[yellow]{clientSyncJsonPath}[/yellow][/bold red]"
        )
        exit(1)

    printr()
    printr("[yellow]Confirming able to access workspace dump directory...[/yellow]")
    workspaceVidsDir:str=join(config.workspaceDir,"videos")
    makedirs(workspaceVidsDir,exist_ok=True)
    if not isdir(workspaceVidsDir):
        printr("[bold red]ERROR: workspace vids dir could not be ensured[/bold red]")
        printr(f"[red]tried to make workspace vids dir at: [yellow]{workspaceVidsDir}[/yellow]")
        exit(1)

elif config.systemType=="client":
    pass