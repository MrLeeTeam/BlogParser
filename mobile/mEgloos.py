from lxml import html
from striper import strip_html as st
from dateutil import parser as DATE
from datetime import date as NOW

import requests


def main():
    print get_article("http://kaengphan.egloos.com/m/11007241")


def get_article(url, mode=None):

    returnee = {}

    if not mode:
        agent = """
        Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us)\
        AppleWebKit/420.1 (KHTML, like Gecko) Version/3.0 Mobile/1A542a Safari/419.3
        """
        structure = requests.get(url, headers={"User-Agent": agent})

    else:
        structure = mode

    charset = structure.encoding

    tree = html.fromstring(structure.text)
    body = tree.cssselect("div.subject")[0]

    returnee["title"] = html.tostring(body.cssselect("h3")[0], encoding=charset, method="text").strip()

    info = html.tostring(body.cssselect("span.name")[0], encoding=charset, method="text");
    returnee["name"] = info.split()[0]
    returnee["date"] = info.split()[1] + " " + info.split()[2]

    article = tree.cssselect("div#post_contents")[0]
    returnee["content"] = st.strip_html(html.tostring(article, encoding=charset, method="html"))
    returnee["images"] = get_images(article)

    return returnee


def get_images(article):
    urls = []

    images = article.cssselect("img")
    for image in images:
        urls.append(image.get("src"))

    return urls


def get_article_list(host, lp=None):
    returnee = []
    re = requests.get(host + "/archives")
    tree = html.fromstring(re.text)
    during = tree.cssselect("ul.f_clear")[0].cssselect("li")

    for month in during:
        flag, page = 1, 1

        while flag:
            req = requests.get(host + "/m" + month.cssselect("a")[0].get("href") + ("/page/%d" % page))
            body = html.fromstring(req.text)

            articles = body.cssselect("ul.category")[0].cssselect("li")
            sw = len(articles)

            for article in articles:
                url = host + article.cssselect("a")[0].get("href")
                a_date = article.cssselect("span.post_info")[0].text
                if not "/" in a_date:
                    current = NOW.today()
                    date = DATE.parse(("%d/%d/%d" % (current.year, current.month, current.day)))

                else:
                    date = DATE.parse(a_date)

                if lp and (date - DATE.parse(lp)).days < 0:
                    flag = 0
                    break

                else:
                    returnee.append(url)

            if sw == 10 and flag == 1:
                page += 1
            elif sw < 10 or flag == 0:
                break

        if flag == 0:
            break

    return returnee


if __name__ == "__main__":
    main()
    # print len(get_article_list("http://cpeuny.egloos.com", "2012/01/01"))