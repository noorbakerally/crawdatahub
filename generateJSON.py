import json
from pyquery import PyQuery as pq
from lxml import etree
import urllib

datahubLink = "https://datahub.io"

def getPageContent(link):
	f = urllib.urlopen(link)
	myfile = f.read()
	return myfile

def getObj(name,obj):
        if name not in obj:
                obj[name] = {}
        return obj[name]

def getdDetails(pagelink):
        pageContent = pq(getPageContent(pagelink))
        title = pageContent.find("div.module-content h1.heading")
        resources = pageContent.find("ul.resource-list .resource-item")
	dObj = {}
        dObj["ExampleItemPageLink"] = []
	nonames = []
        for resource in resources:
                aElement = resource.find("a")
		#print aElement.attrib['href']		
                aContent = aElement.text
                span = aElement.find("span")
                if "example" not in span.attrib["data-format"]:
               		nonames.append(aContent)         
                        continue

                if aContent not in resourceName["name"]:
                        resourceName["name"].append(aContent)
                aLink = aElement.attrib['href']
		fullRLink = "https://datahub.io" + aLink
		rPageContent = pq(getPageContent(fullRLink))
		rurlElement = rPageContent.find("div.module-content p").find("a")
		rurl = rurlElement.text()
		rformat = span.attrib["data-format"]
                dObj["ExampleItemPageLink"].append({"linkName":rurl,"format":rformat})
	resourceName["noname"][pagelink] = nonames
        return dObj


datasets = open('all') 
#datasets = open('test') 
datasets = datasets.readlines()
resourceName = {}
resourceName["name"] = []
resourceName["noname"] = {}
i=1
for link in datasets:
	print i
	obj = {}
	link = link.replace("\n","")
	obj[link] = getdDetails(link)
	filename = str(i)+".json"
	with open(filename, 'w') as outfile:
    		json.dump(obj, outfile)
	i = i + 1
with open('names.json', 'w') as outfile:
    json.dump(resourceName, outfile)
