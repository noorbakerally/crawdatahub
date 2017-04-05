import json
with open("rRepStats.json","r") as inputFile:
	f = json.load(inputFile)

for line in f:
	if f[line]["ATriples"] == "0":
		continue
	lineN = line.replace("//","!!")
	sI = len(lineN)
	if "/" in lineN:
		sI = lineN.index("/")
	print lineN[:sI].replace("!!","//")
