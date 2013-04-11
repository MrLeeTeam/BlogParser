#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2
import re
from bs4 import BeautifulSoup


def strip_html(html):
    p = re.compile(r'<.*?>')

    return p.sub('', html)


def get_article(url):
    page = urllib2.urlopen(url)
    body = page.read()
    encoding = page.headers['content-type'].split('charset=')[-1]
    u_body = unicode(body, encoding)
    bs = BeautifulSoup(u_body)

    # find div.article
    article = bs.find("div", "article")

    images = get_images(article)

    # remove comments in html
    pr1 = re.sub("<!--[\w\W\s]*?-->", "", str(article).replace("&lt;", "<").replace("&gt;", ">"))

    # remove script & contents
    pr2 = re.sub("<script[\w\W\s]*?</script>", "", pr1)

    # remove whitespace (1)
    pr3 = pr2.replace("\n", " ").replace("\t", " ")

    # remove whitespace (2)
    pr4 = re.sub("\s{2,}", " ", pr3.replace(" ", " "))  # 왼쪽거는 c2 a0, 오른쪽거는 20, 한마디로 c2 a0 은 유니코드에서의 화이트스페이스 공백

    # strip html source
    pr5 = strip_html(pr4)

    # Plus divider
    contents = pr5.replace("http", " http")

    return contents, images


def get_images(content):
    images = content.find_all("img")

    returnee = []

    for img in images:
        returnee.append(img.get("src"))

    return returnee


def main():
    # Usage: Look bottom statement
    content, images = get_article("http://linalukas.tistory.com/3986")

    print content
    print "==="
    print images


main()