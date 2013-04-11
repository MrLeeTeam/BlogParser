# -*- coding: utf-8 -*-

from lxml import html
import requests
from striper import strip_html as st


def main():
    article, image_list = get_article("http://cyhome.cyworld.com/?home_id=a3382529&postSeq=8086729&r=popular")
    # article, image_list = get_article("http://blog.cyworld.com/2010spoon/8920744")

    print article
    print "==="
    print image_list


def get_article(url):
    ## Section 0 - Initial set.
    dem = list()
    blog_url = list()
    user_agent = "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13"

    ## Section 1 - Got frame src.
    contents = requests.get(url)
    charset = contents.encoding
    dem.append(html.fromstring(contents.text))

    if "blog.cyworld.com" in url:
        blog_url.append(dem[0][3][3].get("src"))
    else:
        blog_url.append(dem[len(dem) - 1][1][1].get("src"))

        ## Section 2 - Got frame src(2) if not short url.
        contents = requests.get(blog_url[len(blog_url) - 1], headers={"User-Agent": user_agent})
        dem.append(html.fromstring(contents.text))
        blog_url.append(dem[len(dem) - 1][3][3].get("src"))

    ## Section 3 - Got frame src(3).
    contents = requests.get(blog_url[len(blog_url) - 1], headers={"User-Agent": user_agent})
    dem.append(html.fromstring(contents.text))

    for frame in dem[len(dem) - 1].cssselect("iframe"):
        if frame.get("src") and "myhompy" in frame.get("src"):
            blog_url.append("http://web3.c2.cyworld.com" + frame.get("src"))

    ## Section 4 - Got content of article
    contents = requests.get(blog_url[len(blog_url) - 1], headers={"User-Agent": user_agent})
    dem.append(html.fromstring(contents.text))

    article = dem[len(dem) - 1].cssselect("div#myhompy_board_retrieveBoard_contents")[0]
    content = html.tostring(article, encoding=charset, method="html")
    img_list = get_images(article)

    return st.strip_html(content), img_list


def get_images(article):
    img_list = list()
    for image in article.cssselect("img"):
        img_list.append(image.get("src"))

    return img_list


if __name__ == "__main__":
    main()