__author__ = 'jaeyoung'

from lxml import html
from striper import strip_html as st

import requests
import time


def main():
    print get_article("http://haeho.com/m/227")


def get_article(url):

    returnee = dict()
    agent = "Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/420.1 (KHTML, like Gecko) Version/3.0 Mobile/1A542a Safari/419.3"
    now = time.localtime()

    structure = requests.get(url, headers={"User-Agent": agent})
    charset = structure.encoding

    tree = html.fromstring(structure.text)
    body = tree.cssselect("div.wrap_posting")[0]

    returnee["title"] = html.tostring(body.cssselect("div.area_tit h2 a")[0], encoding=charset, method="text")
    info = html.tostring(body.cssselect("span.owner_info")[0], encoding=charset, method="text")
    returnee["name"] = info.split()[0]
    if "/" in info.split()[1]:
        returnee["date"] = info.split()[1] + " " + info.split()[2]
    else:
        returnee["date"] = "%s/%s/%s" % (now.tm_year, now.tm_mon, now.tm_mday) + " " + info.split()[1]

    article = body.cssselect("div.area_content")[0]
    returnee["content"] = st.strip_html(html.tostring(article, encoding=charset, method="html"))
    returnee["images"] = get_images(article)

    return returnee


def get_images(article):
    urls = list()

    images = article.cssselect("img")
    for image in images:
        urls.append(image.get("src"))

    return urls


if __name__ == "__main__":
    main()