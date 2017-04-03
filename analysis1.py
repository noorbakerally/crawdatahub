import json
from rdflib import Graph

def getSubjects(g):
        query = "SELECT DISTINCT ?s WHERE { { ?s ?x ?o . } UNION { ?o ?y ?s .} FILTER (isIRI(?s)) }"
        result = g.query(query)
	return result

def getIndirectionPredicates(g,lName,sName):
        query = "SELECT DISTINCT ?p WHERE { { <"+lName+"> ?p <"+sName+"> . } UNION { <"+sName+"> ?p <"+lName+"> .} }"
        result = g.query(query)
	results = []
	for row in result:
		results.append(row.p)
	return results

with open("cleanlinks.json","r") as cleanLinksFile:
	links = json.load(cleanLinksFile)


with open("rRepStats.json","r") as cleanLinksFile:
	results = json.load(cleanLinksFile)

with open('revfilestatus.json') as data_file:
    rlinkstatus = json.load(data_file)

filesDirectory = "/home/bakerally/Documents/repositories/emse_gitlab/crawdatahub/rfiles/"

numLinkInSubject = 0
indirectionPred = []
for result in results.keys():
	index = links["links"][result]		
	rformat = rlinkstatus[result]
	if "http://el.dbpedia.org/data/Linux.rdf" not in result:
		continue
	g = Graph()
	g = g.parse(filesDirectory+str(index),format=rformat)
	cresult = results[result]

	subjects = getSubjects(g)
        for subject in subjects:
		predicates = getIndirectionPredicates(g,subject.s,result)
		if len(predicates) > 0:
			print predicates
	break
	if cresult["STriples"] == "0" and cresult["OTriples"] == "0":
		print "test"


		subjects = getSubjects(g)
		for subject in subjects:
			if subject.s in result:
				sName = subject.s
				numLinkInSubject = numLinkInSubject + 1
				break
		break
print numLinkInSubject
