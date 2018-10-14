import re
from ftfy import fix_text

def force_unicode(text):
    "If text is unicode, it is returned as is. If it's str, convert it to Unicode using UTF-8 encoding"
    return text if isinstance(text, unicode) else text.decode('utf8')

def clean_spaces(content):
    return fix_text(force_unicode(re.sub("\s\s+", " ", content.strip())))

def clean_date(content):
    return re.sub('([\d]{2})/([\d]{2})/([\d]{4})', '\\3-\\2-\\1', clean_spaces(content))

def clean_datetime(content):
    return re.sub('([\d]{2})/([\d]{2})/([\d]{4}) ([\d]{2})h([\d]{2})', '\\3-\\2-\\1 \\4:\\5:00', clean_spaces(content))

def clean_float(content):
    try:
        return float(re.sub('[^\d.]', '', clean_spaces(content)))
    except ValueError:
        return 0.0

def clean_int(content):
    return int(clean_float(content))

def get_deep_text(node):
    children = node.getchildren()
    return get_deep_text(children[0]) if len(children) > 0 else node.text