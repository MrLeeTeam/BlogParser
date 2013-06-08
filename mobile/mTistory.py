__author__ = 'jaeyoung'


from lxml import html
from striper import strip_html as st
from dateutil import parser as DATE

import requests


import re

def main():
    #a= get_article("http://starter123.tistory.com/m/76")
    #a = get_article("http://black2white.tistory.com/m/post/view/id/4")
    #a = get_article("http://cyborgninja.tistory.com/m/post/view/id/10")
    #a = get_article("http://burnout4.tistory.com/m/post/view/id/32")
    #print a['content']

    #b= get_article_list("http://pongzzang.tistory.com")
    #b = get_article_list("http://rlgns758.tistory.com")
    b = get_article_list("http://markgraf.tistory.com")
    print b

def get_article(url, mode=None):

    returnee = {}

    if not mode:
        agent = "Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/420.1 (KHTML, like Gecko) Version/3.0 Mobile/1A542a Safari/419.3"
        structure = requests.get(url, headers={"User-Agent": agent}, timeout=5.0)

    else:
        structure = mode

    charset = structure.encoding

    tree = html.fromstring(structure.text)
    body = tree.cssselect("div.wrap_posting")[0]

    returnee["title"] = st.refine_text(html.tostring(body.cssselect("div.area_tit h2 a")[0]), encoding=charset)
    owner_info = body.cssselect("span.owner_info")[0]
    date = owner_info.cssselect("span.datetime")[0]

    owner_info.remove(date)

    txt_bars = owner_info.cssselect("span.txt_bar")
    for txt_bar in txt_bars:
        owner_info.remove(txt_bar)

    categories = owner_info.cssselect("span.category_info")
    for cate in categories:
        owner_info.remove(cate)

    name = owner_info

    returnee["name"] = st.refine_text(html.tostring(name), encoding=charset)
    returnee["date"] = DATE.parse(st.refine_text(html.tostring(date), encoding=charset))

    article = body.cssselect("div.area_content")[0]

    scripts = article.cssselect("script")
    for script in scripts:
        script.getparent().remove(script)

    sections = article.cssselect("div.section_writing")
    for section in sections:
        article.remove(section)

    snss = article.cssselect("div.sns")
    for sns in snss:
        article.remove(sns)

    returnee["content"] = st.refine_text(html.tostring(article), encoding=charset).decode("utf8", "ignore").encode("utf8")

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
    flag, page = 1, 1
    returnee = []
    while flag:
        obj = host + "/m/post/list/page/%d" % page
        try:
            re = requests.get(obj, timeout=5.0)
        except Exception:
            continue
        tree = html.fromstring(re.text)

        lists  = tree.cssselect("ul#articleList")
        for list in lists:
            articles =  list.cssselect("li")
            for article in articles:

                alinks = article.cssselect("a")

                if alinks is None or len(alinks) == 0:
                    continue
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
    main()
