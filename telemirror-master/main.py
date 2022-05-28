import logging

from config import (API_HASH, API_ID, CHAT_MAPPING, LOG_LEVEL)
from config import SESSION_STRING, SOURCE_CHATS
from telemirror.mirroring import MirrorTelegramClient

def main():
    logging.basicConfig()
    logger = logging.getLogger(__name__)
    logger.setLevel(level=LOG_LEVEL)

    client = MirrorTelegramClient(SESSION_STRING, API_ID, API_HASH)
    client.configure_mirroring(
        source_chats=SOURCE_CHATS,
        mirror_mapping=CHAT_MAPPING,
        database=True,
        logger=logger
    )
    client.start_mirroring()


if __name__ == "__main__":
    main()
