import wget

f = open("chunklist.m3u8", "r")
f2 = open("links", "w")

lines = f.readlines()

header = "https://link-to-ts-files/"
footer = ""

for line in lines:
    # read from chunklist and concat with header and footer
    # if condition needs to be modified based on platform
    if line.startswith('1080'):
        link = header + line + footer
        f2.write(link)
