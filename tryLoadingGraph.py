import json
from rdflib import Graph
rlinksf = open("rlinks","r")

with open('revfilestatus.json') as data_file:
    rlinkstatus = json.load(data_file)

i=0
rfiles = "/home/bakerally/Documents/repositories/emse_gitlab/crawdatahub/rfiles/"
errors = {}

rRep = {}

for rlink in rlinksf.readlines():
	i = i + 1
	if rlink not in rlinkstatus:
		continue
	rformat = rlinkstatus[rlink]
	
	print str(i) + " " + rformat + " "+ rlink.replace("\n","").encode("utf-8") 
	
	g = Graph()
	try:
		g = g.parse(rfiles+str(i),format=rformat)
	except:
		print rlink
		errors[rlink]=rformat

with open('errorloading.json', 'w') as outfile:
    json.dump(errors, outfile)
