import json
from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef
import sys
reload(sys)
sys.setdefaultencoding('utf8')

with open('rRepStats.json', 'r') as infile:
    data = json.load(infile)
g = Graph()
on = "http://example.com/ontology/"
ON = Namespace("http://example.com/ontology/")
DA = Namespace("http://example.com/data/")
g.bind("on",ON)
g.bind("da",DA)

for rlink in data:
#for rlink in ["http://aemet.linkeddata.es/resource/WeatherStation/id08001?output=ttl"]:
	#print rlink
	rlink = rlink.replace("\n","")
	#print data[rlink]
	linkNode = URIRef(rlink)	

	#define the predicates nodes
	aTripleNode = URIRef(on+"nbATriples")
	sTripleNode = URIRef(on+"nbSTriples")
	oTripleNode = URIRef(on+"nbOTriples")
	gTripleNode = URIRef(on+"nbGTriples")
	#print data[rlink]
	if "PSubject" in data[rlink]:
		pSubject = data[rlink]["PSubject"]
		g.add( (linkNode, ON.pSubject, URIRef(pSubject) ))
		if "PSubjectDetails" in data[rlink]:
			sTriples = data[rlink]["PSubjectDetails"]["STriples"]
			oTriples = data[rlink]["PSubjectDetails"]["OTriples"]
			gTriples = data[rlink]["PSubjectDetails"]["GTriples"]
			g.add( (URIRef(pSubject), sTripleNode, Literal(int(sTriples))) )
        		g.add( (URIRef(pSubject), oTripleNode, Literal(int(oTriples))) )
        		g.add( (URIRef(pSubject), gTripleNode, Literal(int(gTriples))) )

	
	aTriples = data[rlink]["ATriples"]
	sTriples = data[rlink]["STriples"]
	oTriples = data[rlink]["OTriples"]
	gTriples = data[rlink]["GTriples"]
	g.add( (linkNode, RDF.type, ON.WebRDFResource ) )
	g.add( (linkNode, aTripleNode, Literal(int(aTriples))) )
	g.add( (linkNode, sTripleNode, Literal(int(sTriples))) )
	g.add( (linkNode, oTripleNode, Literal(int(oTriples))) )
	g.add( (linkNode, gTripleNode, Literal(int(gTriples))) )
	#break

print g.serialize(format="turtle")
