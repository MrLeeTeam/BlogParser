__author__ = 'jaeyoung'


from lxml import html
from striper import strip_html as st
from dateutil import parser as DATE

import requests

UserAgent = "Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/420.1 (KHTML, like Gecko) Version/3.0 Mobile/1A542a Safari/419.3"



def main():
    #print get_article("http://m.blog.daum.net/phjsunflower/1100")["content"]
    #a = get_article("http://m.blog.daum.net/mpcil/242")
    #print a["content"]
    #a = get_article("http://m.blog.daum.net/_blog/_m/articleView.do?blogid=0AjZA&articleno=17320065&maxNo=17320066&minNo=17320057&maxDt=20090724210224&minDt=20090724185428&maxListNo=17320076&minListNo=17320067&maxListDt=20090729170337&minListDt=20090724210551&currentPage=17&beforePage=16&categoryId=")
    #a = get_article("http://m.blog.daum.net/_blog/_m/articleView.do?blogid=0591M&articleno=5356240&maxNo=13645718&minNo=5356240&maxDt=20080123155844&minDt=20051202160624&maxListNo=15738371&minListNo=15579000&maxListDt=20110107101928&minListDt=20080925175056&currentPage=6&beforePage=5&categoryId=")
    #a = get_article("http://m.blog.daum.net/_blog/_m/articleView.do?blogid=06YrG&articleno=13740502&maxNo=13740504&minNo=13740495&maxDt=20110105210824&minDt=20101014201958&maxListNo=13740518&minListNo=13740505&maxListDt=20110606160706&minListDt=20110202091009&currentPage=4&beforePage=3&categoryId=")
    #print a["content"]


    #b = get_article_list("http://blog.daum.net/eyey-")
    #b = get_article_list("http://blog.daum.net/zellkur")
    b = get_article_list("http://blog.daum.net/harimao22")

    print len(b)

def get_article(url, mode=None):

    returnee = {}

    if not mode:
        structure = requests.get(url, headers={"User-Agent": UserAgent}, timeout=5.0)

    else:
        structure = mode

    charset = structure.encoding

    tree = html.fromstring(structure.text)
    body = tree.cssselect("div#daumContent")[0]

    #print dir(body)

    returnee["title"] = st.refine_text(html.tostring(body.cssselect("p.title")[0]), encoding=charset)
    returnee["name"] = st.refine_text(html.tostring(body.cssselect("span.nick")[0]), encoding=charset)
    returnee["date"] = DATE.parse(st.refine_text(html.tostring(body.cssselect("span.date")[0]), encoding=charset))

    article = body.cssselect("div#article")[0]

    navis = article.cssselect("div.articleNavi")
    for navi in navis:
        navi.getparent().remove(navi)

    rel_articles = article.cssselect("div.relation_article")
    for rel_article in rel_articles:
        rel_article.getparent().remove(rel_article)


    returnee["content"] = st.refine_text(html.tostring(article))

    returnee["images"] = get_images(article)


    post_id = url[url.rfind("/") + 1:]
    post_id = post_id[post_id.find("articleno=") + 10:]
    post_id = post_id[:post_id.find("&")];

    if post_id == '' :
        str = "<meta property=\"og:url\" content=\""
        part = structure.text[structure.text.find(str) + len(str):]
        part = part[:part.find("\"")]
        post_id = part[part.rfind("/") + 1:]
        post_id.encode(charset)

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

        users = tree.cssselect("div.list_by_user")
        for user in users:
            articles = user.cssselect("li")  # get article_list
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