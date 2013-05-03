__author__ = 'jaeyoung'

from mobile import mTistory, mDaum, mEgloos, mNaver
import sys
import requests
import database
import datetime
import signal
# -*- Constant -*-
UserAgent = """
            Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) \
            AppleWebKit/420.1 (KHTML, like Gecko) Version/3.0 Mobile/1A542a Safari/419.3
            """

crawler_id = 0
isKilled = False


def kill(signum, frame):
    global isKilled
    isKilled = True


def init():
    global crawler_id
    if len(sys.argv) < 2:
        print "Usage: %s [crawler id]" % sys.argv[0]
        sys.exit(1)

    signal.signal(signal.SIGINT, kill)
    crawler_id = int(sys.argv[1])
    database.init(crawler_id)


def main():
    while True:
        if isKilled:
            break

        try:
            b_id, host, realm, last_crawl, last_post, succeed = database.get_meta()

            if not succeed:
                print "SUCCEED value false"
                return

            print "[",datetime.datetime.now(), "] : ", host,

            article_list = get_article_list(host, realm, last_post)
            print " [",len(article_list),"]"
            for article in article_list:  # parse article and save to database
                data = get_article(article, realm)
                if len(data) == 0 : continue
                database.save_article(b_id, data)

            database.flag(b_id, 0)  # Unset flag
        except Exception, e:
            print e.message


def get_article_list(host, realm=None, lp=None):
    if host.find("http://") == -1:
        host = "http://" + host
    re = requests.get(host, headers={"User-agent": UserAgent}, timeout=5.0)

    article_list = []
    if re.status_code == 404:
        return article_list
    try:
        if realm == "Tistory" or "tistory.com" in re.text:
            article_list = mTistory.get_article_list(host, lp)
        #
        elif realm == "Daum" or "blog.daum.net" in host:
            article_list = mDaum.get_article_list(host, lp)

        elif realm == "Naver" or "naver.com" in re.text:
            article_list = mNaver.get_article_list(host, lp)

        elif realm == "Egloos" or "egloos.com" in re.text:
            article_list = mEgloos.get_article_list(host, lp)
    except IndexError:
        pass
    return article_list


def get_article(url, realm=None):
    if url.find("http://") == -1:
        url = "http://" + url

    re = requests.get(url, headers={"User-agent": UserAgent}, timeout=5.0)
    data = {}

    if re.status_code == 404:
        return data
    try:
        if realm == "Tistory" or "tistory.com" in re.text:
            data = mTistory.get_article(url, re)

        elif realm == "Daum" or "blog.daum.net" in url:
            data = mDaum.get_article(url, re)

        elif realm == "Naver" or "naver.com" in re.text:
            data = mNaver.get_article(url, re)

        elif realm == "Egloos" or "egloos.com" in re.text:
            data = mEgloos.get_article(url, re)
    except IndexError:
        pass

    return data


if __name__ == "__main__":
    init()
    main()
