# collector sync info
collector sync. collector sync is a set of specific tasks that must be accomplished in order to synchronise the collector with the client.

acts on the following items. these items will all be modified, and must be given to the collector sync function.

- videos dir
- stock dir
- delete dir
- collector anilog
- workspace vids dir

reads from the following:

- client sync json

what it does:

1. reads from client sync json to determine what videos to remove
2. removes the videos specified in client sync json from **videos dir**. the removed videos are placed into the **delete dir**
    - attempts to detect desyncs between client sync json and the videos dir. will cancel if detected any issues
3. moves all vids from **stock** to the **videos dir**. this **empties out the stock dir completely**, so make sure the stock dir only has things that should be moved
4. mirrors all videos from the newly updated **videos dir** to the **workspace videos dir**. this **wipes out the workspace videos dir**, so make sure nothing needed is in there
5. updates the **collector anilog** with all the items that were removed the videos dir, essentially, updating the log with all the items reported by the client
6. create empty file in workspace location to signal client that it needs to mirror new videos to its folder