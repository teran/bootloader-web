import re

RE_TRUE_REGEX = re.compile(
    r'(1|true|yep|yes|yup)', re.IGNORECASE)

def string2bool(string):
    if RE_TRUE_REGEX.match(str(string)):
        return True
    return False
