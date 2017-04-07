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
	if "PResource" in data[rlink]:
		pResource = URIRef(data[rlink]["PResource"])
		pResourceDescNode = BNode()
		g.add( (linkNode, ON.pResourceDesc, pResourceDescNode ))
		g.add( (pResourceDescNode, ON.pResource, pResource ))
		g.add( (pResourceDescNode, RDF.type, ON.PResourceDesc ))
		if "PResourceDetails" in data[rlink]:
			sTriples = data[rlink]["PResourceDetails"]["STriples"]
			oTriples = data[rlink]["PResourceDetails"]["OTriples"]
			gTriples = data[rlink]["PResourceDetails"]["GTriples"]
			g.add( ( pResourceDescNode, sTripleNode, Literal(int(sTriples))) )
        		g.add( ( pResourceDescNode, oTripleNode, Literal(int(oTriples))) )
        		g.add( ( pResourceDescNode, gTripleNode, Literal(int(gTriples))) )
			#g.add( ( pResource, RDF.type, ON.WebRDFResource ) )
			#g.add( ( pResource, RDF.type, ON.PResource ) )
			for pred in data[rlink]["PResourceDetails"]["Relations"]:
				g.add( (pResourceDescNode, ON.pResourcePredicate, URIRef(pred) ) )
	
	aTriples = data[rlink]["ATriples"]
	sTriples = data[rlink]["STriples"]
	oTriples = data[rlink]["OTriples"]
	gTriples = data[rlink]["GTriples"]
	g.add( (linkNode, RDF.type, ON.WebRDFSource ) )
	g.add( (linkNode, aTripleNode, Literal(int(aTriples))) )
	g.add( (linkNode, sTripleNode, Literal(int(sTriples))) )
	g.add( (linkNode, oTripleNode, Literal(int(oTriples))) )
	g.add( (linkNode, gTripleNode, Literal(int(gTriples))) )
	#break

print g.serialize(format="turtle")
