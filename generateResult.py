import json
import traceback
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

def getNumSameTriple(g,resource):
        query = ''' SELECT (count(*) as ?numSame) WHERE 
		{ 
		  { <'''+resource+ '''> ?p <'''+resource+'''> .}
	} '''
        result = g.query(query)
        if (result==None):
                return 0
        for row in result:
                return row.numSame

def getNPopularResource(g,n):
        query = '''select distinct ?s (COUNT(?s) as ?numS ) WHERE {
                   { ?s ?p ?o } UNION { ?o ?p ?s }
		   FILTER (isIRI(?s))
                } 
                GROUP BY ?s 
                ORDER BY DESC (?numS)
                LIMIT ''' + str(n)
	#print query
        subs = []
        result = g.query(query)
        for subject in result:
		#print subject
                subs.append(str(subject.s))
        return subs

def getRelationWithResource(g,r,rlink):
        query = "SELECT DISTINCT ?p WHERE { { <"+rlink+"> ?p <"+r+">} UNION { <"+r+"> ?p <"+rlink+"> } }" 
        #print query
        preds = []
        result = g.query(query)
        for p in result:
                #print subject
                preds.append(str(p.p))
        return preds


with open("cleanlinks.json","r") as cleanLinksFile:
	cleanLinks = json.load(cleanLinksFile)

with open('revfilestatus.json') as data_file:
    rlinkstatus = json.load(data_file)

i=0
rfiles = "/home/bakerally/Documents/repositories/emse_gitlab/crawdatahub/rfiles/"
errors = {}

rRep = {}

counter = 0
for rlink in cleanLinks["links"].keys():
#for rlink in ["http://aims.fao.org/aos/data/c_2724?output=xml","http://aemet.linkeddata.es/resource/WeatherStation/id08001?output=ttl"]:
	#print rlink
	counter = counter + 1
	i = cleanLinks["links"][rlink]	
	
	if rlink not in rlinkstatus.keys():
		continue
	rformat = rlinkstatus[rlink]
	g = Graph()
	try:
		g = g.parse(rfiles+str(i),format=rformat)
		rlink = rlink.replace("\n","")
		aTriples = int(getAllTriples(g))
		STriples = int(getSNumTriples(g,rlink))
		OTriples = int(getONumTriples(g,rlink))
		sameTriples = int(getNumSameTriple(g,rlink))
		rRep[rlink] = {}
		rRep[rlink]["ATriples"] = aTriples
		rRep[rlink]["STriples"] = STriples
		rRep[rlink]["OTriples"] = OTriples
		rRep[rlink]["GTriples"] = aTriples - STriples - OTriples + sameTriples
		pResources = getNPopularResource(g,1)
		if "crawdatahub/rfiles" in pResource:
			rRep[rlink]["PResource"] = rlink
		else:
			#PSubject is a different subject than resource denoted by rlink
			if (len(pResources) > 1):
				pResource = getNPopularResource(g,1)[0]
				rRep[rlink]["PResource"] = pResource
				rRep[rlink]["PResourceDetails"] = {}
				STriples = int(getSNumTriples(g,pResource))
				OTriples = int(getONumTriples(g,pResource))	
				sameTriples = int(getNumSameTriple(g,pResource))
				GTriples = aTriples - STriples - OTriples + sameTriples
				rRep[rlink]["PResourceDetails"]["STriples"] = STriples
				rRep[rlink]["PResourceDetails"]["OTriples"] = OTriples
				rRep[rlink]["PResourceDetails"]["GTriples"] = GTriples
				rRep[rlink]["PResourceDetails"]["Relations"] = getRelationWithResource(g,pResource,rlink)
		print "success:" + str(counter)
		
	except:
		print "error:"
		traceback.print_exc()
		errors[rlink]=rformat
	#break
with open('errorloading.json', 'w') as outfile:
    json.dump(errors, outfile)

with open('rRepStats.json', 'w') as outfile:
    json.dump(rRep, outfile)
