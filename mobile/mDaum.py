__author__ = 'jaeyoung'


from lxml import html
from striper import strip_html as st
from dateutil import parser as DATE

import requests


UserAgent = """
        Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us)\
        AppleWebKit/420.1 (KHTML, like Gecko) Version/3.0 Mobile/1A542a Safari/419.3
        """


def main():
    print get_article("http://blog.daum.net/phjsunflower/1100")


def get_article(url, mode=None):

    returnee = {}

    if not mode:
        structure = requests.get(url, headers={"User-Agent": UserAgent}, timeout=5.0)

    else:
        structure = mode

    charset = structure.encoding

    tree = html.fromstring(structure.text)
    body = tree.cssselect("div#daumContent")[0]

    returnee["title"] = body.cssselect("p.title")[0].text.strip()
    returnee["name"] = body.cssselect("span.nick")[0].text.strip()
    returnee["date"] = DATE.parse(body.cssselect("span.date")[0].text.strip())

    article = body.cssselect("div#article")[0]
    returnee["content"] = st.strip_html(html.tostring(article, encoding="utf8", method="html")).replace("\t", "")
    returnee["images"] = get_images(article)
    post_id = url[url.rfind("/") + 1:]
    post_id = post_id[post_id.find("articleno=") + 10:]
    post_id = post_id[:post_id.find("&")];
    returnee["post_id"] = post_id
    return returnee


def get_images(article):
    urls = []
    images = article.cssselect("img")
    for image in images:
        urls.append(image.get("src"))

    return urls


def get_article_list(host, lp=None):
    returnee = []
    if host.find("http://m.") == -1:
        host = host.replace("http://", "http://m.")

    prefix = "http://m.blog.daum.net"

    current_page, flag, tmp = 1, 1, 1
    next_page = host

    while flag:
        re = requests.get(next_page, headers={"User-Agent": UserAgent}, timeout=5.0)
        tree = html.fromstring(re.text)
        tmp = current_page

        num_pages = tree.cssselect("a.num_box")  # find next page
        for num_page in num_pages:
            chk = "currentPage=%d" % (current_page + 1)
            if chk in num_page.get("href"):
                next_page = prefix + num_page.get("href")
                current_page += 1
                break

        if tmp == current_page:
            flag = 0

        articles = tree.cssselect("div.list_by_user")[0].cssselect("li")  # get article_list
        for article in articles:
            url = prefix + article.cssselect("a")[0].get("href")
            date = article.cssselect("span.date")[0].text
            if lp and (DATE.parse(date) - DATE.parse(lp)).days < 0:
                flag = 0
                break

            else:
                returnee.append(url)

    return returnee

if __name__ == "__main__":
    main()
    # print len(get_article_list("http://blog.daum.net/hamami10", "2012.10.31 08:56"))