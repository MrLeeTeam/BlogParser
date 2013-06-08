from lxml import html
from lxml.html.clean import Cleaner

from striper import strip_html as st
from dateutil import parser as DATE
from datetime import date as NOW

import requests
import time
import datetime


def main():
    #print get_article_list("http://kaengphan.egloos.com")
    #print get_article("http://kaengphan.egloos.com/m/11024115")["content"]

    b = get_article_list("http://gilai.egloos.com")
    print len(b)


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

    header = tree.cssselect("div.subject")[0]

    returnee["title"] = st.refine_text(html.tostring(header.cssselect("h3")[0]), encoding=charset)

    name_date = st.refine_text(html.tostring(header.cssselect("span.name")[0]), encoding=charset)

    name_date = name_date.split()
    returnee["name"] = name_date[0]
    date = " ".join(name_date[1:])


    returnee["date"] = datetime.datetime.now()
    try:
        returnee["date"] = DATE.parse(date)
    except Exception, e:
        print e.message

    article = tree.cssselect("div#post_contents")[0]

    tags = article.cssselect("div.btn_fontsize")
    for tag in tags:
        article.remove(tag)

    cleaner = Cleaner(comments=True)

    returnee["content"] = st.refine_text(html.tostring(cleaner.clean_html(article)), encoding=charset)
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

    prev_list = tree.cssselect("ul.prev_list")

    if prev_list is None or len(prev_list) == 0:
        return returnee
    year_list = prev_list[0].cssselect("li")

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