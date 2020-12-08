# importing required modules

from bs4 import BeautifulSoup
import requests

# getting input from user
disease = input("enter the disease you want to search for : ")

# url for scraping
url = f"https://medlineplus.gov/{disease}.html"
html_content = requests.get(url).text
soup = BeautifulSoup(html_content, "lxml")

# scraping
main_class = soup.find("div", attrs={"id": "topic-summary"})
link = main_class.find("a")

# result
print(main_class.text)
