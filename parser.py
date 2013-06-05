__author__ = 'jaeyoung'

from mobile import mTistory, mDaum, mEgloos, mNaver
from core import logger

import sys
import requests
import database
import signal
# -*- Constant -*-
UserAgent = "Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/420.1 (KHTML, like Gecko) Version/3.0 Mobile/1A542a Safari/419.3"

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
                logger.log("Getting blog entity is failed")
                return

            try:
                article_list = get_article_list(host, realm, last_post)
            except Exception, e:
                logger.log(e.message, host)
                database.flag_rollback(b_id)
                continue

            logger.log(host, " [", len(article_list), "]")
            success_count = 0
            for article in article_list:

                try:
                    data = get_article(article, realm)
                except Exception, e:
                    logger.log(e.message, article)
                    continue

                if len(data) == 0:
                    continue
                if database.save_article(b_id, data):
                    success_count += 1

            logger.log(success_count, "accepted")
            database.flag(b_id, 0)

        except Exception, e:
            logger.log(b_id, "global error:", e.message)
            database.flag_rollback(b_id)



def get_article_list(host, realm=None, lp=None):
    if "http://" not in host:
        host = "http://" + host
    re = requests.get(host, headers={"User-agent": UserAgent}, timeout=5.0)

    article_list = []
    if re.status_code == 404:
        return article_list
    try:
        if realm == "Tistory" or "tistory.com" in host:
            article_list = mTistory.get_article_list(host, lp)
        #
        elif realm == "Daum" or "blog.daum.net" in host:
            article_list = mDaum.get_article_list(host, lp)

        elif realm == "Naver" or "naver.com" in host:
            article_list = mNaver.get_article_list(host, lp)

        elif realm == "Egloos" or "egloos.com" in host:
            article_list = mEgloos.get_article_list(host, lp)
    except IndexError, e:
        logger.log("get article_list failed", e.message)
        raise IndexError(e.message)

    return article_list


def get_article(url, realm=None):
    if "http://" not in url:
        url = "http://" + url

    re = requests.get(url, headers={"User-agent": UserAgent}, timeout=5.0)
    data = {}

    if re.status_code == 404:
        return data
    try:
        if realm == "Tistory" or "tistory.com" in url:
            data = mTistory.get_article(url, re)

        elif realm == "Daum" or "blog.daum.net" in url:
            data = mDaum.get_article(url, re)

        elif realm == "Naver" or "naver.com" in url:
            data = mNaver.get_article(url, re)

        elif realm == "Egloos" or "egloos.com" in url:
            data = mEgloos.get_article(url, re)
    except IndexError, e:
        logger.log("get article failed - ", e.message)

    return data


if __name__ == "__main__":
    init()
    main()
