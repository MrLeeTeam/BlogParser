# -*- coding: utf-8 -*-

from lxml import html
from striper import strip_html as st


def main():
    article, images = get_article("http://blog.daum.net/shoesu/5886217")

    print article
    print "==="
    print images


def get_article(url):
    ## Section 0 - Initial set.
    blog_url = list()
    dem = list()

    ## Section 1 - Got frame src.
    dem.append(html.parse(url).getroot())
    blog_url.append("http://blog.daum.net" + dem[0][1][0].attrib["src"])
    # print "[System] Got blog-url[1] from iframe successfully. :", blog_url[0]

    ## Section 2 - Get frame src(2).
    dem.append(html.parse(blog_url[0]).getroot())
    frames = dem[1].cssselect("iframe")
    for frame in frames:
        if "if_b" in frame.get("name"):
            blog_url.append("http://blog.daum.net" + frame.get("src"))
    # print "[System] Got blog-url[2] from iframe successfully. :", blog_url[1]

    ## Section 3 - Get contents of article.
    dem.append(html.parse(blog_url[1]).getroot())
    article = dem[2].cssselect("div#contentDiv")[0]

    img_links = get_images(article)

    ## Section 4 - Return data.
    return st.strip_html(html.tostring(article, encoding="utf-8", method="html")), img_links


def get_images(article):
    img_links = list()
    for image in article.cssselect("img"):
        img_links.append(image.get("src"))

    return img_links


if __name__ == "__main__":
    main()