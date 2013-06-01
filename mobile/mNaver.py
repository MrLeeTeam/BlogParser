from lxml import html
from striper import strip_html as st

import requests
import time
import datetime
from dateutil import parser as DATE


def main():
    print get_article("http://m.blog.naver.com/cik0131/150169028112")


def get_article(url, mode=None):

    returnee = {}
    now = time.localtime()

    if not mode:
        agent = "Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/420.1 (KHTML, like Gecko) Version/3.0 Mobile/1A542a Safari/419.3"
        structure = requests.get(url, headers={"User-Agent": agent}, timeout=5.0)

    else:
        structure = mode

    charset = structure.encoding


    tree = html.fromstring(structure.text)
    body = tree.cssselect("div#ct")[0]

    returnee["title"] = html.tostring(body.cssselect("div.end_tt h2")[0], encoding=charset, method="text")

    returnee["name"] = html.tostring(body.cssselect("div.end_tt p span a ")[0], encoding=charset, method="text")
    date = datetime.datetime.now()
    try:
        date = DATE.parse(html.tostring(body.cssselect("div.end_tt p span.s_tm")[0], encoding=charset, method="text"))
    except:
        pass
    returnee["date"] = date

    try:
        article = body.cssselect("div.post_tx div")[0]
    except:
        article = body.cssselect("div.post_tx p")[0]
    returnee["content"] = st.strip_html(html.tostring(article, encoding="utf8", method="html"))
    returnee["images"] = get_images(article)
    returnee["post_id"] = url[url.rfind("/")+1:]

    return returnee


def get_article_list(host, lp=None):
    import re
    returnee = []

    flag, page = 1, 1

    if host.find("http://m.") == -1:
        host = host.replace("http://", "http://m.")

    while flag:
        obj = host + "?currentPage=%s" % page
        try:
            req = requests.get(obj, timeout=5.0)
        except:
            print "time out"
            continue
        curPage = re.search("currentPage : ([0-9]+),", req.text)

        if curPage is not None and int(curPage.group(1)) == page:
            tree = html.fromstring(req.text)

            articles = tree.cssselect("ul.blog_u")[0].cssselect("li")

            for article in articles:
                post_id = article.get("id")
                post_id = "/" + post_id.replace("postLi_", "")
                returnee.append(host + post_id)

            page += 1

        else:
            flag = 0;

    return returnee




def get_images(article):
    urls = []

    images = article.cssselect("img")
    for image in images:
        urls.append(image.get("src"))

    return urls


if __name__ == "__main__":
    main()