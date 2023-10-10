# phase 3 client sync
this sync occurs after collector has synced to the workspace (phase 2). the client now needs to sync with the collector's new update

1. mirrors videos from workspace into client vids dir, completely replacing all vids in
client vids dir
2. modifies client's anilog file, removing all seperators. adds a new seperator at the top of the
file
3. removes videos-available.txt, preventing client sync from collector again