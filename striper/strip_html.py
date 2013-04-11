__author__ = 'jaeyoung'

import re


def strip_html(html):
    data = re.sub("<script[\w\W\s]*?</script>", "", html)
    data = re.sub("<style[\w\W\s]*?</style>", "", data)
    p = re.compile(r'<.*?>')
    data = p.sub('', data)

    return data.strip()

