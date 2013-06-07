from lxml import html
from striper import strip_html as st

import requests
import time
import datetime
from dateutil import parser as DATE


def main():
    try:
        #a= get_article("http://m.blog.naver.com/zeminica7/80009913680")
        #a= get_article("http://m.blog.naver.com/cyber3208/60163282137")
        #print a["content"]
        #b = get_article_list("http://blog.naver.com/skye20")
        #b= get_article_list("http://blog.naver.com/ulmink")

        print len(b)
    except Exception, e:
        print "error", e.message
    #list = get_article_list("http://m.blog.naver.com/zeminica7", None)
    #for p in list:
     #   try:
      #      print get_article(p)
       # except:
        #    print p


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

    title = body.cssselect("div.end_tt h2")[0]
    title.remove(title.cssselect("a")[0])

    returnee["title"] = st.refine_text(html.tostring(title), encoding=charset)

    returnee["name"] = st.refine_text(html.tostring(body.cssselect("div.end_tt p span a")[0]), encoding=charset)

    date = datetime.datetime.now()
    try:
        date = DATE.parse(st.refine_text(html.tostring(body.cssselect("div.end_tt p span.s_tm")[0]), encoding=charset))
    except Exception, e:
        pass
    returnee["date"] = date

    article = body.cssselect("div.post_tx")[0]
    article.remove(article.cssselect("span.ut_txt")[0])

    returnee["content"] = st.refine_text(html.tostring(article), encoding=charset)

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


            groups = tree.cssselect("ul.blog_u")
            for group in groups:
                articles = group.cssselect("li")

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