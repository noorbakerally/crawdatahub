import urllib2
import json
import os.path


rfile = open("rlinks","r")
#rfile = open("test","r")
rlines = rfile.readlines()
fileStatus = {}
i=1

#where the file will be actually stored
partURL="/home/bakerally/Documents/repositories/emse_gitlab/crawdatahub/rfiles/"

for rline in rlines:
	rline = rline.split(" ")[0]
		
	#new name for the downloaded file
	newFileName = partURL + str(i)
	print str(i)+"  "+rline

	#if (os.path.isfile(newFileName)):
		#continue
	
	
	request = urllib2.Request(rline, headers={"Accept" : "text/turtle,application/rdf+xml,text/ntriples,application/ld+json"})

	try:
		response = urllib2.urlopen(request,timeout=4)
		content = response.read()
		contentType = response.info().getheader('Content-Type')
		
		rout = open(newFileName,"w")
		rout.write(content)
		rout.close()

		if "xml" in contentType:
			contentType = "xml"
		elif "turtle" in contentType:
			contentType = "turtle"
		elif "n3" in contentType:
			contentType = "n3"
		elif "nt" in contentType:
			contentType = "nt"

		if contentType not in fileStatus.keys():
			fileStatus[contentType] = []
		fileStatus[contentType].append(rline)
	
	except:
		if "error" not in fileStatus.keys():
                        fileStatus["error"] = []
                fileStatus["error"].append(rline)
	i = i + 1

with open('filestatus.json', 'w') as outfile:
    json.dump(fileStatus, outfile)
