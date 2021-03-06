import re

from api.models import Search
from api.helpers import r


def create_comics_list(q, lang):
    comics_list = r.get("comic_list_%s" % lang)
    if not comics_list:
        t = "%s_title" % lang
        title_list = Search.values_list(t, flat=True)
        comics_list = list(set(title_list))
        r.setex("comic_list_%s" % lang, comics_list, 24 * 60 * 60)  # todo 过期时间 24*60*60(一天)
    comics_list = eval(comics_list) if isinstance(comics_list, bytes) else comics_list
    availed_list = ["", None]
    comics_list = list(set(comics_list).difference(set(availed_list)))
    suggestions = []
    pattern = '.*?'.join(q.lower())
    regex = re.compile(pattern)
    for item in comics_list:
        match = regex.search(item)
        if match:
            suggestions.append((len(match.group()), match.start(), item))
    return [x for _, _, x in sorted(suggestions[:10])]
