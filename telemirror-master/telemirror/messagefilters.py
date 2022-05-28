import re
from abc import abstractmethod
from typing import List, Protocol, Set, Union

from telethon import custom, types
from urlextract import URLExtract

MessageLike = Union[types.Message, custom.Message]


class MesssageFilter(Protocol):
    @abstractmethod
    def process(self, message: MessageLike) -> MessageLike:
        raise NotImplementedError


class EmptyMessageFilter(MesssageFilter):

    def process(self, message: MessageLike) -> MessageLike:
        return message


class UrlMessageFilter(MesssageFilter):

    def __init__(
        self: 'UrlMessageFilter',
        placeholder: str = '***',
        filter_mention: bool = True,
        blacklist: Union[List[str], Set[str]] = {},
        whitelist: Union[List[str], Set[str]] = {}
    ) -> None:
        self._placeholder = placeholder
        self._filter_mention = filter_mention
        self._extract_url = URLExtract()
        self._extract_url.permit_list = blacklist
        if not blacklist:
            self._extract_url.ignore_list = whitelist

    def process(self, message: MessageLike) -> MessageLike:
        # replace plain text
        message.message = self._filter_urls(message.message)
        # remove MessageEntityTextUrl
        if message.entities is not None:
            message.entities = [
                e for e in message.entities
                if not(isinstance(e, types.MessageEntityTextUrl) and self._extract_url.has_urls(e.url))
            ]
        return message

    def _filter_urls(self, text: str) -> str:
        urls = self._extract_url.find_urls(text, only_unique=True)
        for url in urls:
            text = text.replace(url, self._placeholder)

        if self._filter_mention:
            text = re.sub(r'@[\d\w]*', self._placeholder, text)

        return text


class RestrictSavingContentBypassFilter(MesssageFilter):

    def process(self, message: MessageLike) -> MessageLike:
        raise NotImplementedError


class SequenceMessageFilter(MesssageFilter):

    def __init__(self, *arg: MesssageFilter) -> None:
        self._filters = list(arg)

    def process(self, message: MessageLike) -> MessageLike:
        for f in self._filters:
            message = f.process(message)
        return message