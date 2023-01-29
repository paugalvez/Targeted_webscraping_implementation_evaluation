import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

def getIfExists(elem):
    return elem.text.strip() if elem else None


def getDataFromUrl(url):
    r = requests.get(url)
    if isinstance(r.text, str) and "An Error Occurred" in r.text:
        return None
    soup = bs(r.text, "html.parser")

    title = getIfExists(soup.find("h2"))
    description = getIfExists(soup.find('div', {'id': 'descResumen'}))
    updatedOn = getIfExists(soup.find('div', {'id': 'fechaact'}))
    location = soup.find_all('li', class_= "margin-bottom-10")
    locations = []
    for i in location:
        tempo = i.string
        locations.append(tempo)
    categories_asset = soup.find_all('img', class_='float-left cateimages')
    categories = []
    for i in categories_asset:
        temp = i['title']
        categories.append(temp)

    return title, description, updatedOn, ",".join(locations) if locations and len(locations) else None, ",".join(categories) if categories and len(categories) else None,


df = pd.DataFrame(columns=[
    "title",
    "description",
    "updatedOn",
    "locations",
    "categories",


])

for index in range(0,30000):
    currentActivity = getDataFromUrl(f"https://activosdesalud.com/recurso/show/{index}/cat")
    if currentActivity is None:
        continue
    #print(currentActivity)
    df.loc[len(df.index)] = currentActivity
    df.to_csv("recursosdes23122022.csv", index=False)
    if index % 100 == 0:
        print(index)



