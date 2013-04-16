__author__ = 'jaeyoung'


from mobile import mTistory, mDaum, mEgloos, mNaver

import requests
import psycopg2 as psycopg2

# -*- Constant -*-
UserAgent = """
            Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) \
            AppleWebKit/420.1 (KHTML, like Gecko) Version/3.0 Mobile/1A542a Safari/419.3
            """

CRAWLER_ID = 1

def main():
    b_id, host, realm, last_crawl, last_post, succeed = get_meta()
    if succeed == False:
        print "SUCCEED value false"
        return
    #flag(h_id, 1)  # Set flag
    article_list = get_article_list(host, realm, last_post)

    for article in article_list:  # parse article and save to database
        data = get_article(article, realm)
        save(data, b_id)

    flag(b_id, 0)  # Unset flag


def get_meta():  # Set Flag, Get Host, Get Realm, Get Date

    b_id = None
    url = None
    realm = None
    last_crawl = None
    last_post = None
    succ_flag = False

    conn = None
    try:
        conn = psycopg2.connect(host="61.43.139.115", database="mrlee", user="mrlee", password="altmxjfl")
        cursor = conn.cursor()
        cursor.execute("select b_id, url, realm, last_crawl, last_post from blog_meta where  (crawler_id is null or crawler_id = 0) and realm not in ('Daum', 'Naver') order by last_crawl  limit 1")

        record = cursor.fetchone()
        if record:
            b_id, url, realm, last_crawl, last_post = record
            succ_flag = True

            cursor.execute("UPDATE blog_meta set crawler_id = %d where b_id = %d " % (CRAWLER_ID, b_id))
            conn.commit()


    except:
        print "get meta error"
        if conn:
            conn.rollback()

    finally:
        if conn:
            conn.close()

    return b_id, url, realm, last_crawl, last_post, succ_flag


def flag(b_id, sw):
    # ids = ""
    # for ido in h_id:
    #     ids += "%s" % ido if len(ids) == 0 else ",%s" % ido
    #
    # if sw == 0:
    #     # Unset Flag
    #     pass
    #
    # elif sw == 1:
    #     # Set Flag
    #     pass

    conn = None
    try:
        conn = psycopg2.connect(host="61.43.139.115", database="mrlee", user="mrlee", password="altmxjfl")
        cursor = conn.cursor()

        cursor.execute("UPDATE blog_meta set crawler_id = 0 where b_id = %d " % (b_id))
        conn.commit()

    except:
        print "set flag error"
        if conn:
            conn.rollback()

    finally:
        if conn:
            conn.close()


def get_article_list(host, realm=None, lp=None):
    if host.find("http://") == -1:
        host = "http://" + host
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


def save(data, b_id):  # Save data to db
    conn = None
    try:
        conn = psycopg2.connect(host="61.43.139.115", database="mrlee", user="mrlee", password="altmxjfl")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO blog_data(b_id, post_id, author, title, postdate, contents) values(%s, %s, %s, %s, %s, %s)", [b_id, data["post_id]"], data["name"], data["title"], data["date"], data["content"]])
        conn.commit()

    except:
        print "## save error"

    finally:
        if conn:
            conn.close()


def get_article(url, realm=None):
    if url.find("http://") == -1:
        url = "http://" + url

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