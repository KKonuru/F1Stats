import requests
from bs4 import BeautifulSoup 
import urllib.request


def getDrivers():
    url  = "https://www.formula1.com/en/drivers.html"
    data = requests.get(url)
    drivers = list()
    soup = BeautifulSoup(data.text,'html.parser')
    for x in soup.find_all("a",class_="driver"):
        firstName = x.find_all("span",class_="firstname")
        LastName = x.find_all("span",class_="lastname")
        drivers.append(firstName[0].string+" "+LastName[0].string)
    return drivers

def getImages():
    url = "https://www.formula1.com/en/drivers.html"
    data = requests.get(url)
    images = list()
    soup = BeautifulSoup(data.text,"html.parser")
    for x in soup.find_all("a",class_="listing-item--link"):
        picture = x.find("picture",class_="listing-item--photo")
        img = picture.find("img")
        images.append(img["data-src"])
    return images

images = getImages()
print(images)




    