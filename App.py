import pandas as pd
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, send_file, request, session, redirect, url_for
from flask_session import Session

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

datas = []

urlTarget = requests.get(
    "https://www.mncvision.id/article/index/-/all")
beautify = BeautifulSoup(urlTarget.content, "html.parser")
articles = beautify.find_all("div", class_="latest-wrapper clearfix")
for article in articles:
    getThumbnail = article.find("img", class_="img-responsive")
    getCategory = article.find("a", class_="tag").text
    getDate = article.find("span", class_="pull-right").text
    getTitle = article.find("h3", class_="news-title").text
    getLink = article.find("a")

    # format document
    datas.append({
        "thumbnail": getThumbnail["src"],
        "title": getTitle,
        "category": getCategory,
        "date": getDate,
        "link": getLink["href"]
    })


@app.route('/')
def index():
    try:
        if not session.get("name"):
            return redirect(url_for('login'))
        return render_template("index.html", datas=datas)

    except Exception as err:
        return "Error: {}".format({err})


@app.route("/detail/", methods=["POST"])
def newsDetail():
    try:
        newsDetails = []

        getUrlTarget = request.form["getUrl"]
        urlTarget = requests.get(getUrlTarget)
        beautify = BeautifulSoup(urlTarget.content, "html.parser")
        parentElement = beautify.find("div", class_="detail")

        getTitle = parentElement.find("h1", class_="page-header").text
        getCategory = parentElement.find(
            "a", class_="label label-default tm tm-category").text
        getViews = parentElement.findAll("small")[0].text
        getDate = parentElement.findAll("small")[1].text
        getCoverImage = parentElement.find(
            "img", class_="article-img img-responsive")
        getContent = parentElement.find("div", class_="text-full").text

        newsDetails.append({
            "title": getTitle,
            "category": getCategory,
            "views": getViews,
            "date": getDate,
            "coverImage": getCoverImage["src"],
            "content": getContent
        })

        return render_template("detail.html", newsDetails=newsDetails, title=getTitle)

    except Exception as err:
        return "Error: {}".format({err})


@app.route("/read/<string:getCategory>")
def readNews(getCategory):
    newsByCategory = []

    for data in datas:
        if data["category"] == getCategory:
            newsByCategory.append(data)

    return render_template("category.html", newsByCategory=newsByCategory, title=getCategory)


@app.route("/download")
def download():
    fileName = "data.csv"
    getFile = pd.DataFrame(datas)
    getFile.to_csv(fileName, encoding="utf-8")
    return send_file(fileName, as_attachment=True)


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session["name"] = request.form.get("name")
        return redirect(url_for("index"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session["name"] = None
    return redirect(url_for("index"))
