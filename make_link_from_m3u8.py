import wget

f = open("chunklist.m3u8", "r")
f2 = open("links", "w")

lines = f.readlines()

header = "https://a01-g-naver-vod.pstatic.net/navertv/c/read/v2/VOD_ALPHA/navertv_2021_02_14_227/hls/"

footer = "?__gda__=1613350993_fadb6a8f4987d19edcdfcaf33cb57400"

for line in lines:

    if line.startswith('1080'):
        link = header + line + footer
        f2.write(link)
