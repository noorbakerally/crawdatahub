import json
with open('filestatus.json', 'r') as infile:
    filestatus = json.load(infile)
newfilestatus = {}
fformats = ["xml","turtle","n3","application/ld+json"]
for fformat in fformats:
	rlines = filestatus[fformat]
	for rline in rlines:
		newfilestatus[rline] = fformat

with open('revfilestatus.json', 'w') as outfile:
    json.dump(newfilestatus, outfile)
