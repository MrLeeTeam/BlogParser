__author__ = 'jaeyoung'


import requests
from mobile import mTistory, mDaum


def main():
    url, realm = get_url() ## get url from db
    data = separator(url, realm)

    save(data)


def get_url():
    # Get url from database
    return "http://haeho.com/m/227", None


def save(data):
    # Save data to DB
    pass


def separator(url, realm=None):
    agent = "Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/420.1 (KHTML, like Gecko) Version/3.0 Mobile/1A542a Safari/419.3"
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