__author__ = 'jaeyoung'

import re
import HTMLParser
html_parser = HTMLParser.HTMLParser()

def strip_html(html):
    data = re.sub("<script[\w\W\s]*?</script>", "", html)
    data = re.sub("<style[\w\W\s]*?</style>", "", data)
    data = re.sub("<br[ /]?>", "\n", data)
    data = re.sub("<p( [^>]*>|>)", "\n", data)
    p = re.compile(r'<.*?>')
    data = p.sub('', data)

    return html_parser.unescape(data.strip())


def refine_text(text, encoding=None):
    text = strip_html(text)
    text = text.replace("\r", "").strip()
    if encoding:
        text = text.encode(encoding)
    return text