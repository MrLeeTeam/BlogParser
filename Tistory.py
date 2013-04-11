# -*- coding: utf-8 -*-

from lxml import html
from striper import strip_html as st
import requests


def main():
    article, image_list = get_article("http://hwsecter.tistory.com/450?_top_tistory=new_title#.UV8SQ6uPgqs")

    print article
    print "==="
    print image_list


def get_article(url):
    contents = requests.get(url)
    charset = contents.encoding
    tree = html.fromstring(contents.content)
    article = tree.cssselect("div.article")[0]
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