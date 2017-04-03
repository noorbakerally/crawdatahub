import json
from rdflib import Graph

def getSNumTriples(g,resource):
        query = "SELECT (count(*) as ?numS) WHERE { <"+resource+"> ?x ?o}"
        result = g.query(query)
        if (result==None):
                return 0
        for row in result:
                return row.numS

def getONumTriples(g,resource):
        query = "SELECT (count(*) as ?numO) WHERE { ?s ?x <"+resource+">}"
        result = g.query(query)
        if (result==None):
                return 0
        for row in result:
                return row.numO

def getAllTriples(g):
        query = "SELECT (count(*) as ?numA) WHERE { ?s ?x ?y .}"
        result = g.query(query)
        if (result==None):
                return 0
        for row in result:
                return row.numA

with open("cleanlinks.json","r") as cleanLinksFile:
	cleanLinks = json.load(cleanLinksFile)

with open('revfilestatus.json') as data_file:
    rlinkstatus = json.load(data_file)

i=0
rfiles = "/home/bakerally/Documents/repositories/emse_gitlab/crawdatahub/rfiles/"
errors = {}

rRep = {}

for rlink in cleanLinks["links"].keys():
	i = cleanLinks["links"][rlink]	
	
	if rlink not in rlinkstatus.keys():
		continue
	rformat = rlinkstatus[rlink]
	g = Graph()
	try:
		g = g.parse(rfiles+str(i),format=rformat)
		rlink = rlink.replace("\n","")
		aTriples = getAllTriples(g)
		STriples = getSNumTriples(g,rlink)
		OTriples = getONumTriples(g,rlink)
		rRep[rlink] = {}
		rRep[rlink]["ATriples"] = aTriples
		rRep[rlink]["STriples"] = STriples
		rRep[rlink]["OTriples"] = OTriples
		
		print "success:"
		
	except:
		print "error:"
		errors[rlink]=rformat

with open('errorloading.json', 'w') as outfile:
    json.dump(errors, outfile)

with open('rRepStats.json', 'w') as outfile:
    json.dump(rRep, outfile)
