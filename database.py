import psycopg2
import datetime


con = None
crawler_id = None


def init(cr_id):
    global con
    global crawler_id

    con = psycopg2.connect(host="58.229.105.83", database="mrlee", user="mrlee", password="altmxjfl")
    crawler_id = cr_id


def save_article(b_id, data):
    global con
    result = False
    try:

        cursor = con.cursor()

        cursor.execute("SELECT article_id, b_id, post_id from blog_data where b_id = %s and post_id = %s", [b_id, data["post_id"]])

        row = cursor.fetchone()
        if row is None:
            cursor.execute("INSERT INTO blog_data(b_id, post_id, author, title, crawl_date, post_date, contents) values(%s, %s, %s, %s, %s, %s, %s)", [b_id, data["post_id"], data["name"], data["title"], datetime.datetime.now(), data["date"], data["content"]])
            con.commit()
            result = True

            image_list = [[b_id, data["post_id"], url, datetime.datetime.now()] for url in data["images"]]
            for image in image_list:
                cursor.execute("INSERT INTO blog_image(b_id, post_id, image_url, crawl_date) VALUES(%s, %s, %s, %s)", image)
                con.commit()
        else:
            a_id, b_id, p_id = row
            cursor.execute("UPDATE blog_data set contents = %s , crawl_date = %s, post_date = %s where article_id = %s", [data["content"], datetime.datetime.now(), data["date"], a_id])
            con.commit()
            result = True

    except Exception, e:
        print "## save error : %s " % e.message
        con.rollback()
    return result


def flag_rollback(b_id):
    global con

    try:
        cursor = con.cursor()

        cursor.execute("UPDATE blog_meta set crawler_id = 0 where b_id = %s", b_id)
        con.commit()

    except:
        print "rollback flag error"
        if con:
            con.rollback()


def flag(b_id, sw):
    global con

    try:
        cursor = con.cursor()

        cursor.execute("UPDATE blog_meta set crawler_id = 0, last_crawl = %s where b_id = %s", [datetime.datetime.now(), b_id])
        con.commit()

    except:
        print "set flag error"
        if con:
            con.rollback()


def get_meta():  # Set Flag, Get Host, Get Realm, Get Date
    global con
    global crawler_id
    b_id = None
    url = None
    realm = None
    last_crawl = None
    last_post = None
    succ_flag = False

    try:
        cursor = con.cursor()
        cursor.execute("select * from get_noncrawled_meta()")

        record = cursor.fetchone()
        if record:
            b_id, url, realm, last_crawl, last_post = record
            succ_flag = True

    except:
        print "get meta error"
        if con:
            con.rollback()

    return b_id, url, realm, last_crawl, last_post, succ_flag
