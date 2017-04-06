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
	#print rlink
	rlink = rlink.replace("\n","")
	aTriples = data[rlink]["ATriples"]
	sTriples = data[rlink]["STriples"]
	oTriples = data[rlink]["OTriples"]
	gTriples = data[rlink]["GTriples"]
	linkNode = URIRef(rlink)	
	aTripleNode = URIRef(on+"nbATriples")
	sTripleNode = URIRef(on+"nbSTriples")
	oTripleNode = URIRef(on+"nbOTriples")
	gTripleNode = URIRef(on+"nbGTriples")
	
	g.add( (linkNode, RDF.type, ON.WebRDFResource ) )
	g.add( (linkNode, aTripleNode, Literal(int(aTriples))) )
	g.add( (linkNode, sTripleNode, Literal(int(sTriples))) )
	g.add( (linkNode, oTripleNode, Literal(int(oTriples))) )
	g.add( (linkNode, gTripleNode, Literal(int(gTriples))) )
	#break
print g.serialize(format="turtle")
