__author__ = 'jaeyoung'


from lxml import html
import time
import requests


def main():
    now = time.localtime()
    reg_date = "%s%s%s000000" % (now.tm_year, now.tm_mon, now.tm_mday)

    get_article_list("0CETz", reg_date)


def get_article_list(blog_id, time_set):
    url = "http://blog.daum.net/_blog/BlogTypeMain.do?blogid=%s&alllist=Y&dispkind=B2202&currentPage=5&maxregdt=%s&minregdt=%s" % (blog_id, time_set, time_set)
    a = requests.get(url)
    page = html.fromstring(a.content)

    print a.content


if __name__ == "__main__":
    main()

