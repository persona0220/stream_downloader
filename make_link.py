f = open("links", "w")

header = "https://link-to-ts-files"

footer = ".ts"

for i in range(1, 330, 1):
    link = header + str(i) + footer + "\n"
    f.write(link)
