import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json
import requests
from bs4 import BeautifulSoup
url = "https://socialblade.com/youtube/"
html = requests.get(url)
print (html.text[:500])
soup = BeautifulSoup(html.text)
body = soup.findAll("div", {"class": "table-body"})


def prepare_table_row(row):
    first = [i.text for i in row if i != u'\n']
    return dict(rank=int(first[0]),
                grade=str(first[1]),
                channel=str(first[2]),
                videos=float(first[3].replace(",", "")),
                subscribers=float(first[4].replace(",", "")),
                views=float(first[5].replace(",", ""))
                )


print(prepare_table_row(body[0]))

data = []
for tr in body:
    datum = prepare_table_row(tr)
    for a in tr.find_all('a', href=True):
        datum['url'] = a['href']
    data.append(datum)

df = pd.DataFrame(data)
print(df)

# now let's plot the results we got
# this plot shows the subscribers of channels
ax = sns.barplot(x=df["subscribers"], y=df["channel"])
plt.show()
# this plot show the views of the channels
ax1 = sns.barplot(x=df["views"], y=df["channel"])
plt.show()
