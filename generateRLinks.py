import json
i=1
stop = 858
rurl = "/home/bakerally/Documents/repositories/emse_gitlab/crawdatahub/jsonwithrurl/"
for i in range(1,stop):
	rfile = open(rurl+str(i)+".json","r")
	rContent = json.loads(rfile.read())
	ks = rContent.keys()	
	for r in rContent[ks[0]]["ExampleItemPageLink"]:
		print r["linkName"].encode('utf-8')
		
	
