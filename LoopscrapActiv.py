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
    populationTarget = getIfExists(soup.find('div', {'id': 'diana'}))
    location = getIfExists(soup.find('div', {'id': 'lugar'}))
    organizations = getIfExists(soup.find('div', {'id': 'centro'}))
    updatedOn = getIfExists(soup.find('div', {'id': 'fechaact'}))
    typeAsset = getIfExists(soup.find('div', {'id': 'sitatual'}))
    isFree = getIfExists(soup.find('div', {'id': 'gratuita'}))
    try:
        duration = getIfExists(soup.find('div', {'id': 'fechainicio'}))
    except Exception as e:
        # print(e)
        duration = None
    # length = (duration.text)

    categories_asset = soup.find_all('img', class_='float-left cateimages')
    categories = []
    for i in categories_asset:
        temp = i['title']
        categories.append(temp)

    return title, description, populationTarget, location, organizations, updatedOn, typeAsset, isFree, ",".join(categories) if categories and len(categories) else None, duration


df = pd.DataFrame(columns=[
    "title",
    "description",
    "populationTarget",
    "location",
    "organizations",
    "updatedOn",
    "typeAsset",
    "is_free",
    "categories",
    "time_activity",

])

for index in range(0, 30000):
    currentActivity = getDataFromUrl(f"https://activosdesalud.com/actividad/show/{index}/cat")
    if currentActivity is None:
        continue
    #print(currentActivity)
    df.loc[len(df.index)] = currentActivity
    df.to_csv("FinalAct231222.csv", index=False)
    if index % 100 == 0:
        print(index)


