# "Qewert1i"
from bs4 import BeautifulSoup
import requests

response = requests.get("https://www.rbc.ru/")
soup = BeautifulSoup(response.text, "html.parser")
news = soup.find("span", class_="main__feed__title-wrap")
print(news.text)
