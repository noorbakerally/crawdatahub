import json
from rdflib import Graph
from texttable import Texttable
import math

import sys  
reload(sys)  
sys.setdefaultencoding('utf8')

def printStable(sArray):
	#print "Triple Category"
	#print "==============="
	t = Texttable()
	t.add_rows([['Rep', 'ST','OT',"Cases","% Cases"]])	
	for rep in sArray.keys():
		crep = sArray[rep]
		pNumCase = (float(crep["NumCase"])/totalCases)*100
		t.add_row([rep,crep["ST"],crep["OT"],crep["NumCase"],pNumCase])	
	t.add_row(['','','Total',totalCases,''])
	return t.draw()


def getSocRowArray(label,i,sArray):
	cases = sArray[str(i)]["Cases"]
	pCases = (float(cases)/totalCases) * 100
	sLinkCase = sArray[str(i)]["SLink Case"]
	pSLinkCase = sArray[str(i)]["PSLink Case"]
	return [label,cases,pCases,sLinkCase,pSLinkCase]
def printSocTable(sArray):
	#print "Subject Occurence Table"
	#print "========================"

	i=0;
	t = Texttable()
	t.add_rows([['% STriples', 'Cases', "% Cases","SLink Cases","PSLink Cases"]])
	
	t.add_row(getSocRowArray("0",0,sArray))
	for i in range(1,10):
		StriplePLabel = ">" + str(i-1) + "0 & <=" + str(i) + "0" 
		StriplePLabel = StriplePLabel.replace("00","0")
		t.add_row(getSocRowArray(StriplePLabel,i,sArray))
	t.add_row(getSocRowArray(">= 90",10,sArray))
	return t.draw()
		

def getNPopularSubject(g,n):
	query = '''select distinct ?s (COUNT(?s) as ?numS ) WHERE {
		   ?s ?p ?o 
		} 
		GROUP BY ?s 
		ORDER BY DESC (?numS)
		LIMIT ''' + str(n)
	subs = []
	result = g.query(query)
	for subject in result:
		subs.append(str(subject.s))
	return subs
def hasLinktoPSubject(g,subs,rlink):
	pred = []
	for s in subs:
		query = "SELECT ?p WHERE { { <"+rlink+"> ?p <"+s+"> .} UNION { <"+s+"> ?p <"+rlink+"> .}}"
		result = g.query(query)
		for r in result:
			pred.append(str(r.p))
	return pred

def getSLink(g,rlink):
	query = "SELECT ?p WHERE {{ <"+rlink+"> ?p ?o} UNION { ?x ?p <"+rlink+"> }}"
	result = g.query(query)
	pred = []
	for p in result:
		pred.append(str(p.p))
	return pred

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

subOc = {  
	"0":{"Cases":0,"% Cases":0,"SLink Case":0,"% SLink Case":0,"PSLink Case":0,"% PSLink Case":0},
	"1":{"Cases":0,"% Cases":0,"SLink Case":0,"% SLink Case":0,"PSLink Case":0,"% PSLink Case":0},
	"2":{"Cases":0,"% Cases":0,"SLink Case":0,"% SLink Case":0,"PSLink Case":0,"% PSLink Case":0},
	"3":{"Cases":0,"% Cases":0,"SLink Case":0,"% SLink Case":0,"PSLink Case":0,"% PSLink Case":0},
	"4":{"Cases":0,"% Cases":0,"SLink Case":0,"% SLink Case":0,"PSLink Case":0,"% PSLink Case":0},
	"5":{"Cases":0,"% Cases":0,"SLink Case":0,"% SLink Case":0,"PSLink Case":0,"% PSLink Case":0},
	"6":{"Cases":0,"% Cases":0,"SLink Case":0,"% SLink Case":0,"PSLink Case":0,"% PSLink Case":0},
	"7":{"Cases":0,"% Cases":0,"SLink Case":0,"% SLink Case":0,"PSLink Case":0,"% PSLink Case":0},
	"8":{"Cases":0,"% Cases":0,"SLink Case":0,"% SLink Case":0,"PSLink Case":0,"% PSLink Case":0},
	"9":{"Cases":0,"% Cases":0,"SLink Case":0,"% SLink Case":0,"PSLink Case":0,"% PSLink Case":0},
	"10":{"Cases":0,"% Cases":0,"SLink Case":0,"% SLink Case":0,"PSLink Case":0,"% PSLink Case":0} }

stemplate = {"Cases":0,"% Cases":0,"SLink":0,"PSLink":0}

fileProcessed = 0
popularPredicates = ""
for result in results.keys():
	
	fileProcessed = fileProcessed + 1
	print fileProcessed

	index = links["links"][result]
        rformat = rlinkstatus[result]

	#if (result != "le"):	
	#if ("-sady/65186030%3E&default-graph-" in result):
		#continue

	cresult = results[result]
	if cresult["ATriples"] == "0":
		continue


	totalCases = totalCases + 1
	index = links["links"][result]		
	rformat = rlinkstatus[result]

	if cresult["STriples"] == "0" and cresult["OTriples"] == "0":
		sCases["GT"]["NumCase"] = sCases["GT"]["NumCase"] + 1			

	elif cresult["STriples"] != "0" and cresult["OTriples"] == "0":
		sCases["ST"]["NumCase"] = sCases["ST"]["NumCase"] + 1			
	
	elif cresult["STriples"] != "0" and cresult["OTriples"] != "0":
		sCases["SOT"]["NumCase"] = sCases["SOT"]["NumCase"] + 1			
	
	elif cresult["STriples"] == "0" and cresult["OTriples"] != "0":
		sCases["OT"]["NumCase"] = sCases["OT"]["NumCase"] + 1			

	aTriples = int(cresult["ATriples"])
	sTriples = int(cresult["STriples"])
	oTriples = int(cresult["OTriples"])
	
	#performing a classification based on categorisation	
	pS = (float(sTriples)/float(aTriples)) * 100
	
	#pS=0 always
	if cresult["STriples"] == "0":
		subOc["0"]["Cases"] = subOc["0"]["Cases"] + 1
		continue
	
	pS = int(math.ceil(pS))
	sPs = str(pS)
	pS = int(math.ceil(int(sPs) / 10))
	subOc[str(pS)]["Cases"] = subOc[str(pS)]["Cases"] + 1

	#load graph
        g = Graph()
        g = g.parse(filesDirectory+str(index),format=rformat)
	
	#check if rlink is related to a IRI resource in the graph
	pred = getSLink(g,result)
	if (len(pred) > 0):
		subOc[str(pS)]["SLink Case"] = subOc[str(pS)]["SLink Case"] + 1

	#get most n popular subject
	n = 1
	p = getNPopularSubject(g,1)
	#check if rlink is related to the n popular subject
	pred = hasLinktoPSubject(g,p,result)
	if (len(pred) > 0):
                subOc[str(pS)]["PSLink Case"] = subOc[str(pS)]["PSLink Case"] + 1
		for p in pred:
			if p not in popularPredicates:
				popularPredicates = popularPredicates + "\n" + p


rs = printStable(sCases)	
#print subOc
rs = rs + "\n" + printSocTable(subOc) + "\n\n"

f = open("analysis_result","w")
f.write(rs)
f.write("Popular Predicates:"+popularPredicates)
f.close()


















