from re import match, search,Match
from devtools import debug

# with open("a.txt","r") as rfile:
#     while True:
#         line:str=rfile.readline()

#         res:Match|None=search("(---)+",line)
#         if res:
#             print("found",line)
#             print(res)

#         if not line:
#             exit()

text:str="2023-09-19 01:14:55 [Glue] Amanchu! - 08 [BD 1080p][9E2F1C78].mkv"
# text:str="=="
res=match(
    r"(\d+-\d+-\d+ \d+:\d+:\d+) (.*)",
    text
)

if not res:
    print("ad")
    exit()

print(res)
print(res[2])
