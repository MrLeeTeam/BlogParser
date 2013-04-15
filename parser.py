__author__ = 'jaeyoung'


from mobile import mTistory, mDaum, mEgloos, mNaver

import requests
import psycopg2cffi as psycopg2

# -*- Constant -*-
UserAgent = """
            Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) \
            AppleWebKit/420.1 (KHTML, like Gecko) Version/3.0 Mobile/1A542a Safari/419.3
            """


def main():
    h_id, host, realm, last_crawl, last_post = get_meta()
    flag(h_id, 1)  # Set flag
    article_list = get_article_list(host, realm, last_post)

    for article in article_list:  # parse article and save to database
        data = get_article(article, realm)
        save(data, h_id)

    flag(h_id, 0)  # Unset flag


def get_meta():  # Set Flag, Get Host, Get Realm, Get Date
    conn = None
    try:
        conn = psycopg2.connect(host="61.43.139.115", database="mrlee", user="mrlee", password="altmxjfl")
        cursor = conn.cursor()
        cursor.execute("select * from blog_meta order by las_crawl where crawler_id < 1 limit 10")

        record = cursor.fetch_all()

    except conn:
        print "err"

    h_id = 22
    host = "http://haeho.com/m/227"
    realm = ""
    last_crawled = ""
    last_post = ""

    return h_id, host, realm if realm else None, last_crawled if last_crawled else 0, last_post


def flag(h_id, sw):
    ids = ""
    for ido in h_id:
        ids += "%s" % ido if len(ids) == 0 else ",%s" % ido

    if sw == 0:
        # Unset Flag
        pass

    elif sw == 1:
        # Set Flag
        pass


def get_article_list(host, realm=None, lp=None):
    re = requests.get(host, headers={"User-agent": UserAgent})
    article_list = []

    if realm == "Tistory" or "tistory.com" in re.text:
        article_list = mTistory.get_article_list(host, lp)
    #
    # elif realm == "Daum" or "blog.daum.net" in host:
    #     pass
    #
    # elif realm == "Naver" or "naver.com" in re.text:
    #     pass

    elif realm == "Egloos" or "egloos.com" in re.text:
        article_list = mEgloos.get_article_list(host, lp)

    return article_list


def save(data, h_id):  # Save data to db
    pass


def get_article(url, realm=None):
    re = requests.get(url, headers={"User-agent": UserAgent})
    data = {}

    if realm == "Tistory" or "tistory.com" in re.text:
        data = mTistory.get_article(url, re)

    elif realm == "Daum" or "blog.daum.net" in url:
        data = mDaum.get_article(url, re)

    elif realm == "Naver" or "naver.com" in re.text:
        data = mNaver.get_article(url, re)

    elif realm == "Egloos" or "egloos.com" in re.text:
        data = mEgloos.get_article(url, re)

    return data


if __name__ == "__main__":
    main()
    # flag(["15", "19", "20", "26", "27", "29"], 0)