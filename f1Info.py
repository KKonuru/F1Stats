import requests
from bs4 import BeautifulSoup
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




    