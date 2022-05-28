from config import API_HASH, API_ID, SESSION_STRING
from telemirror.mirroring import MirrorTelegramClient

with MirrorTelegramClient(api_id=API_ID, api_hash=API_HASH) as client:
    client.print_session_string()
    client.session_string == SESSION_STRING
