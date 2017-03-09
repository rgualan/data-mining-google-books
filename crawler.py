import json
from datetime import datetime
from bs4 import BeautifulSoup
from html2json.html2json import extract, collect

# Read an html file
file_data = open('input/gap-html/gap_2X5KAAAAYAAJ/00000065.html','r').read()
page = BeautifulSoup(file_data, "lxml")
#print(page)

# Convert from html to json
with open("input/template.json") as f:
    template = json.load(f)
    #print(template)
data = collect(page, template)
#data["fileName"] = "Some nanem"
#data["Crawling Date"] = datetime.now().strftime("%B %-d, %Y")

#print(data)
print(json.dumps(data, indent=4, sort_keys=True))