
f = open("links", "w")

header = "https://a01-g-naver-vod.pstatic.net/navertv/c/read/v2/VOD_ALPHA/navertv_2021_02_14_227/hls/4bded24d-6e5d-11eb-89de-625f9a4201fc-"

footer = ".ts?__gda__=1613350993_fadb6a8f4987d19edcdfcaf33cb57400"

for i in range(1, 330, 1):
    link = header + str(i) + footer + "\n"
    f.write(link)
