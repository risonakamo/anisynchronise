# phase actions
## phase 1
- dont do if client status json already existing
- client writes status to workspace sync dir
- add seperator to log file?
    - could also wait until phase 3?

## phase 2
- if there is no client json in sync dir, do nothing
- collector log file updated by reading sync dir
- based on update, vid files moved to delete dir
    - if any vids missing, cancel the move, and warn user of any items that are missing
    - compute the resulting vid file list after the sync. if the list is different from the client's vid file list, mention something, and cancel the move
- sync complete. move all files from stock folder to vids dir
- mirror-copy vids dir to sync workspace vids dir
- clean up workspace sync dir, removing the client's json
- write a file to signal the client should do phase 3

## phase 3
- if sync dir has signal file, perform phase 3
- mirror-copy sync workspace vids dir to vids dir