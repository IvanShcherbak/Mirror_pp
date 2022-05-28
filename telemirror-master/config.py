from decouple import config, Csv

# telegram app id
API_ID: str = config("API_ID")
# telegram app hash
API_HASH: str = config("API_HASH")


def cast_mapping(v: str) -> dict:
    mapping = {}

    if not v:
        return mapping

    import re

    matches = re.findall(
        r'\[?((?:-100\d+,?)+):((?:-100\d+,?)+)\]?', v, re.MULTILINE)
    for match in matches:
        sources = [int(val) for val in match[0].split(',')]
        targets = [int(val) for val in match[1].split(',')]
        for source in sources:
            mapping.setdefault(source, []).extend(targets)
    return mapping


# channels mapping
# [source:target1,target2];[source2:...]
CHAT_MAPPING: dict = config("CHAT_MAPPING", cast=cast_mapping, default="")

if not CHAT_MAPPING:
    raise Exception("The chat mapping configuration is incorrect.")

# channels id to mirroring
SOURCE_CHATS: list = list(CHAT_MAPPING.keys())

# auth session string: can be obtain by run login.py
SESSION_STRING: str = config("SESSION_STRING")







LOG_LEVEL: str = config("LOG_LEVEL", default="INFO").upper()
