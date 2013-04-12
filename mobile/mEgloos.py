from lxml import html
from striper import strip_html as st

import requests
import time


def main():
    print get_article("http://kaengphan.egloos.com/m/11007241")


def get_article(url, mode=None):

    returnee = {}
    now = time.localtime()

    if not mode:
        agent = "Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/420.1 (KHTML, like Gecko) Version/3.0 Mobile/1A542a Safari/419.3"
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


if __name__ == "__main__":
    main()