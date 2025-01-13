import re


def remove_html_tags(text: str) -> str:
    regex = re.compile(r'<.*?>')
    text = re.sub(regex, '', text)
    return re.sub("  ", " ", text)
