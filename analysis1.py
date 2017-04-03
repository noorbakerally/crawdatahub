import json
from rdflib import Graph
from texttable import Texttable

def printStable(sArray):
	print "Triple Category"
	print "==============="
	t = Texttable()
	t.add_rows([['Rep', 'ST','OT',"NumCase","PNumCase"]])	
	for rep in sArray.keys():
		crep = sArray[rep]
		pNumCase = (float(crep["NumCase"])/totalCases)*100
		t.add_row([rep,crep["ST"],crep["OT"],crep["NumCase"],pNumCase])	
	t.add_row(['','','Total',totalCases,''])
	print t.draw()

def getPopularSubject(g):
	query = '''select distinct ?s (COUNT(?s) as ?numS ) WHERE {
		   ?s ?p ?o 
		} 
		GROUP BY ?s 
		ORDER BY DESC (?numS)
		LIMIT 1'''
	result = g.query(query)
	for subject in result:
		return subject.s


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
totalCases = 0

sCases = {"GT":{"ST":"=0","OT":"=0","NumCase":0,"PNumCase":7},
	  "ST":{"ST":">0","OT":"=0","NumCase":0,"PNumCase":7},
	  "SOT":{"ST":">0","OT":">0","NumCase":0,"PNumCase":7},
	  "OT":{"ST":"=0","OT":">0","NumCase":0,"PNumCase":7} }

for result in results.keys():
	cresult = results[result]
	if cresult["ATriples"] == "0":
		continue
	
	totalCases = totalCases + 1
	index = links["links"][result]		
	rformat = rlinkstatus[result]
	#g = Graph()
	#g = g.parse(filesDirectory+str(index),format=rformat)

	if cresult["STriples"] == "0" and cresult["OTriples"] == "0":
		sCases["GT"]["NumCase"] = sCases["GT"]["NumCase"] + 1			

	elif cresult["STriples"] != "0" and cresult["OTriples"] == "0":
		sCases["ST"]["NumCase"] = sCases["ST"]["NumCase"] + 1			
	
	elif cresult["STriples"] != "0" and cresult["OTriples"] != "0":
		sCases["SOT"]["NumCase"] = sCases["SOT"]["NumCase"] + 1			
	
	elif cresult["STriples"] == "0" and cresult["OTriples"] != "0":
		sCases["OT"]["NumCase"] = sCases["OT"]["NumCase"] + 1			


printStable(sCases)	



















