import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import csv
data = []
with open('you.csv') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    datum = {}
    for idx, row in enumerate(reader):
        mod = (idx % 6)
        if mod < 5:

            if mod == 0:
                datum['grade'] = str(row[0])
            elif mod == 1:
                datum['channel'] = str(row[0])
            elif mod == 2:
                datum['uploads'] = int(row[0].replace(
                    ',', '')) if row[0] != '--' else 0
            elif mod == 3:
                datum['subscribers'] = int(row[0].replace(
                    ',', '')) if row[0] != '--' else 0
            elif mod == 4:
                datum['views'] = int(row[0].replace(
                    ',', '')) if row[0] != '--' else 0
            else:
                data.append(datum)
                datum = {}
df = pd.DataFrame(data)
df.head()
df.to_csv('formatted_youtube_data.csv')

#print (idx, row)
