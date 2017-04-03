import urllib2
import json

with open('filestatus.json') as data_file:    
    data = json.load(data_file)

errors = data["error"]
print len(errors)

rfile = open("rlinks","r")
rlines = rfile.readlines()
i=0
for rline in rlines:
 	i = i + 1
	if rline not in errors:
		continue
	print rline
	rlineNoS = rline.split(" ")[0].replace("\n","")

	request = urllib2.Request(rlineNoS, headers={"Accept" : "text/turtle,application/rdf+xml,text/ntriples,application/ld+json"})
	try:
                response = urllib2.urlopen(request,timeout=5)
                content = response.read()
                contentType = response.info().getheader('Content-Type')

                rout = open("/home/bakerally/Documents/repositories/emse_gitlab/crawdatahub/rfiles/"+str(i),"w")
                rout.write(content)
                rout.close()

		errors.remove(rline)
		if contentType not in fileStatus.keys():
                        fileStatus[contentType] = []
                fileStatus[contentType].append(rline)
		print "appended"
        except:
		pass
data["error"] = errors
with open('filestatus.json', 'w') as outfile:
    json.dump(data, outfile)
