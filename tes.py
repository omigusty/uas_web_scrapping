from bs4 import BeautifulSoup
import requests

newsDetails = []


urlTarget = requests.get(
    "https://www.mncvision.id/article/read/content_article/1672919048/tayangan-unggulan-bulan-januari-temani-imlek-di-rumah")
beautify = BeautifulSoup(urlTarget.content, "html.parser")
parentElement = beautify.find("div", class_="detail")

getTitle = parentElement.find("h1", class_="page-header").text
getCategory = parentElement.find(
    "a", class_="label label-default tm tm-category").text
getviews = parentElement.findAll("small")[0].text
getDate = parentElement.findAll("small")[1].text
getContent = parentElement.find("div", class_="text-full").text
getCoverImage = parentElement.find(
    "img", class_="article-img img-responsive")
print(getCoverImage["src"])
