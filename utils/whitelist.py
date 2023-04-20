import re

RE_WHITELIST = [
    r"/health",
    r"/user/send-code",
    r"/user/register",
    r"/user/login",
    r"/user/generate-image",
    r"/user/check-code"
]

WHITELIST = [re.compile(i) for i in RE_WHITELIST]


def check_whitelist(path):
    for w in WHITELIST:
        if w.match(path):
            return True
    return False
