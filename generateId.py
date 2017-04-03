import sys  
reload(sys)  
sys.setdefaultencoding('utf8')

import json
from rdflib import Graph
rlinksf = open("rlinks_cleaned","r")



with open('revfilestatus.json') as data_file:
    rlinkstatus = json.load(data_file)

rlinks = rlinksf.readlines()

print "http://vocab.nerc.ac.uk/collection/P08/current/\n" in rlinks

#for rlink in rlinkstatus.keys():
#	if rlink not in rlinks:
#		print rlink
#		break
