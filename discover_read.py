import json
import sys
import csv
"""
if sys.argv[1] is not None and sys.argv[2] is not None:

    fileInput = sys.argv[1]
    fileOutput = sys.argv[2]

    inputFile = open("discover-data.json", encoding="utf8")
    outputFile = open("discover_csv.csv", 'w')
    data = json.load(inputFile)
    inputFile.close()

    output = csv.writer(outputFile)

    output.writerow(data[1].keys())  # header row

    for row in data:
        output.writerow(row.values())
"""
'''
f = open("discover-data.json") data = json.load(f) f.close()

f= csv.writer(open('discover_csv.csv','wb+'))

for item in data:
    f.writerow([item['pk'], item['model']] + item['fields'].values())'''

json_parsed = json.loads("discover-data.json")
