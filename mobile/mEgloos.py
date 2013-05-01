from lxml import html
from striper import strip_html as st
from dateutil import parser as DATE
from datetime import date as NOW

import requests
import time


def main():
    print get_article_list("http://kaengphan.egloos.com")


def get_article(url, mode=None):

    returnee = {}
    now = time.localtime()

    if not mode:
        agent = """
        Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us)\
        AppleWebKit/420.1 (KHTML, like Gecko) Version/3.0 Mobile/1A542a Safari/419.3
        """
        structure = requests.get(url, headers={"User-Agent": agent}, timeout=5.0)

    else:
        structure = mode

    charset = structure.encoding

    tree = html.fromstring(structure.text)
    body = tree.cssselect("div.subject")[0]

    returnee["title"] = html.tostring(body.cssselect("h3")[0], encoding=charset, method="text").strip()

    info = html.tostring(body.cssselect("span.name")[0], encoding=charset, method="text");
    returnee["name"] = info.split()[0]
    if len(info) > 2:
        returnee["date"] = info.split()[1] + " " + info.split()[2]
    else:
        import datetime
        returnee["date"] = datetime.datetime.now()
    article = tree.cssselect("div#post_contents")[0]
    returnee["content"] = st.strip_html(html.tostring(article, encoding="utf8", method="html"))
    returnee["images"] = get_images(article)
    returnee["post_id"] = url[url.rfind("/")+1:]

    return returnee


def get_images(article):
    urls = []

    images = article.cssselect("img")
    for image in images:
        urls.append(image.get("src"))

    return urls


def get_article_list(host, lp=None):
    returnee = []
    re = requests.get(host + "/m/archives", timeout=5.0)
    tree = html.fromstring(re.text)
    year_list = tree.cssselect("ul.prev_list")[0].cssselect("li")

    for year in year_list:
        year_url = year.get("onclick")
        year_url = year_url.replace("location.href=", "").replace("'", "");

        year_re = requests.get(host + year_url, timeout=5.0)
        year_tree = html.fromstring(year_re.text)

        month_list = year_tree.cssselect("ul.prev_list")[0].cssselect("li")

        for month in month_list:
            month_url = month.get("onclick")
            month_url = month_url.replace("location.href=", "").replace("'", "");

            month_re = requests.get(host + month_url, timeout=5.0)
            month_tree = html.fromstring(month_re.text)

            post_list = month_tree.cssselect("ul.category")[0].cssselect("li")
            for post in post_list:
                post_url = post.cssselect("a")[0].get("href")
                returnee.append(host + post_url)

    return returnee


if __name__ == "__main__":
    main()
    # print len(get_article_list("http://cpeuny.egloos.com", "2012/01/01"))