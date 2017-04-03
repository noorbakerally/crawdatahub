import sys  
import json

reload(sys)  
sys.setdefaultencoding('utf8')

rlinksf = open("rlinks","r")
rlinks = rlinksf.readlines()

rlinkscf = open("rlinks_cleaned","w")
cleanlinks = {"links":{},"links_rev":{}}
i = 0
for rlink in rlinks:
	i = i + 1
	rlink = rlink.split(" ")[0]
	rlink = rlink.encode("utf-8")
	rlinkscf.write(rlink)	
	rlink = rlink.replace("\n","")
	cleanlinks["links"][rlink] = i
	cleanlinks["links_rev"][i] = rlink
	print i
rlinkscf.close()

with open('cleanlinks.json', 'w') as outfile:
    json.dump(cleanlinks, outfile)
