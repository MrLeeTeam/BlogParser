__author__ = 'jaeyoung'


from lxml import html
from striper import strip_html as st
from dateutil import parser as DATE

import requests


def main():
    print get_article("http://blog.daum.net/phjsunflower/1100")


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
    body = tree.cssselect("div#daumContent")[0]

    returnee["title"] = body.cssselect("p.title")[0].text.strip()
    returnee["name"] = body.cssselect("span.nick")[0].text.strip()
    returnee["date"] = DATE.parse(body.cssselect("span.date")[0].text.strip())

    article = body.cssselect("div#article")[0]
    returnee["content"] = st.strip_html(html.tostring(article, encoding=charset, method="html")).replace("\t", "")
    returnee["images"] = get_images(article)
    returnee["post_id"] = url[url.rfind("/")+1:]
    return returnee


def get_images(article):
    urls = []
    images = article.cssselect("img")
    for image in images:
        urls.append(image.get("src"))

    return urls


if __name__ == "__main__":
    main()
