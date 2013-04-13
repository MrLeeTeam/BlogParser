__author__ = 'jaeyoung'


from mobile import mTistory, mDaum

import requests
import psycopg2cffi as psycopg2


def main():
    data = {}
    h_id, host, realm, last_crawled, last_post = get_meta()
    flag(h_id, 1)
    article_list = get_article_list(host, last_post)

    for article in article_list:
        data = separator(article, realm)

    save(data, host)
    flag(h_id, 0)


def get_meta():  # Set Flag, Get Host, Get Realm, Get Date
    conn = None
    try:
        conn = psycopg2.connect(host="61.43.139.115", database="mrlee", user="mrlee", password="altmxjfl")
        cursor = conn.cursor()
        cursor.execute("select * from blog_meta order by las_crawl where crawler_id < 1 limit 10")

        record = cursor.fetch_all()

    except conn:
        print "err"
        pass

    h_id = 22
    host = "http://haeho.com/m/227"
    realm = ""
    last_crawled = ""
    last_post = ""

    return h_id, host, realm if realm else None, last_crawled if last_crawled else 0, last_post


def flag(h_id, sw):
    if sw == 0:
        # Unset Flag
        pass

    elif sw == 1:
        # Set Flag
        pass


def get_article_list(host, lc, lp):
    pass


def save(data, url):  # Save data to db
    pass


def separator(url, realm=None):
    agent = """
    Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us)\
    AppleWebKit/420.1 (KHTML, like Gecko) Version/3.0 Mobile/1A542a Safari/419.3
    """
    re = requests.get(url, headers={"User-agent": agent})
    data = {}

    if realm == "Tistory" or "tistory.com" in re.text:
        data = mTistory.get_article(url, re)

    elif realm == "Daum" or "blog.daum.net" in url:
        data = mDaum.get_article(url, re)

    elif realm == "Naver" or "naver.com" in re.text:
        pass

    elif realm == "Egloos" or "egloos.com" in re.text:
        pass

    return data


if __name__ == "__main__":
    main()