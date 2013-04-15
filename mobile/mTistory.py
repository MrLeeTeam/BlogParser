__author__ = 'jaeyoung'


from lxml import html
from striper import strip_html as st
from dateutil import parser as DATE

import requests


def main():
    print get_article("http://lovegadget.tistory.com/1383")


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
    body = tree.cssselect("div.wrap_posting")[0]

    returnee["title"] = html.tostring(body.cssselect("div.area_tit h2 a")[0], encoding=charset, method="text")
    info = html.tostring(body.cssselect("span.owner_info")[0], encoding=charset, method="text")
    returnee["name"] = info.split()[0]
    returnee["date"] = DATE.parse(info.split()[1])

    article = body.cssselect("div.area_content")[0]
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
    flag, page = 1, 1
    returnee = []
    while flag:
        obj = host + "/m/post/list/page/%d" % page
        re = requests.get(obj)
        tree = html.fromstring(re.text)

        articles = tree.cssselect("ul#articleList")[0].cssselect("li")

        for article in articles:
            url = host + article.cssselect("a")[0].get("href")
            if lp and (DATE.parse(article.cssselect("span.datetime")[0].text) - DATE.parse(lp)).days < 0:
                flag = 0
                break

            else:
                returnee.append(url)

        if not "tPostController.getPost" in re.text or not "nextPage" in re.text:
            flag = 0

        # print page, "Page Complete!"
        page += 1

    return returnee


if __name__ == "__main__":
    # main()
    # articles = get_article_list("http://imuky.tistory.com")
    articles = get_article_list("http://ansanstory.com", "2012/03/17 15:20")
    print articles