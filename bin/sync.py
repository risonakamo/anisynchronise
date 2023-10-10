# main sync program. reads config to determine what type of computer to choose sync task

from os import makedirs
from os.path import dirname,realpath,join,isdir,isfile
from loguru import logger
from rich import print as printr

from anisynchronise.client_sync import clientSyncFromCollector, genClientSyncToFile
from anisynchronise.config import loadConfig

from anisynchronise.types.config_types import ClientConfig, CollectorConfig

@logger.catch()
def main():
    HERE:str=dirname(realpath(__file__))

    configFilePath:str=join(HERE,"../config/config.yml")
    if not isfile(configFilePath):
        printr("[bold red]ERROR: Could not find config.yml. Check readme.md for setup instructions")
        exit(1)

    config:CollectorConfig|ClientConfig=loadConfig(join(HERE,"../config/config.yml"))

    # ------ collector action -------
    if config.systemType=="collector":
        printr("[magenta]--- System Type: [cyan]Collector[/cyan] ---[/magenta]")

        if not isdir(config.workspaceDir):
            printr("[bold red]ERROR: Failed to access workspace dir")
            printr(f"Expected workspace dir at: {config.workspaceDir}")
            exit(1)

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



    # ------- client actions --------
    elif config.systemType=="client":
        printr("[magenta]--- System Type: [cyan]Client[/cyan] ---[/magenta]")

        if not isdir(config.workspaceDir):
            printr("[bold red]ERROR: Failed to access workspace dir")
            printr(f"Expected workspace dir at: {config.workspaceDir}")
            exit(1)

        # ------- phase 1 sync --------
        if not isfile(join(config.workspaceDir,"videos-available.txt")):
            printr("[cyan]Performing Client Sync Phase 1: Writing Client Json[/cyan]")
            printr()

            genClientSyncToFile(
                vidDir=config.clientVideosDir,
                anilogFile=config.clientAnilogFile,
                outputFile=join(config.workspaceDir,"client-sync.json")
            )



        # ------- phase 3 sync --------
        else:
            printr("[cyan]Performing Client Sync Phase 3: Sync from Collector[/cyan]")

            clientSyncFromCollector(
                workspaceDir=config.workspaceDir,
                videosDir=config.clientVideosDir,
                anilogFile=config.clientAnilogFile
            )

if __name__=="__main__":
    main()