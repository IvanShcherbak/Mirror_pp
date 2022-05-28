import collections
import logging
from abc import abstractmethod
from contextlib import contextmanager
from typing import List, Protocol

from psycopg2 import pool
from psycopg2.extensions import AsIs, ISQLQuote, adapt


class MirrorMessage:
    def __init__(self, original_id: int, original_channel: int,
                 mirror_id: int, mirror_channel: int):
        self.original_id = original_id
        self.mirror_id = mirror_id
        self.original_channel = original_channel
        self.mirror_channel = mirror_channel

    def __str__(self):
        return f'{self.__class__}: {self.__dict__}'

    def __repr__(self):
        return self.__str__()

    def __conform__(self, protocol):
        if protocol is ISQLQuote:
            return self.__getquoted()
        return None

    def __getquoted(self):
        _original_id = adapt(self.original_id).getquoted().decode('utf-8')
        _original_channel = adapt(
            self.original_channel).getquoted().decode('utf-8')
        _mirror_id = adapt(self.mirror_id).getquoted().decode('utf-8')
        _mirror_channel = adapt(
            self.mirror_channel).getquoted().decode('utf-8')
        return AsIs(f'{_original_id}, {_original_channel}, {_mirror_id}, {_mirror_channel}')


class Database(Protocol):
    """
    Base database class

    Provides two user functions that work messages mapping data:
    - Add new `MirrorMessage` object to database
    - Get `MirrorMessage` object from database by original message ID
    """

    @abstractmethod
    def insert(self: 'Database', entity: MirrorMessage) -> None:
        """Inserts `MirrorMessage` object into database

        Args:
            entity (`MirrorMessage`): `MirrorMessage` object
        """
        raise NotImplementedError

    @abstractmethod
    def get_messages_to_edit(self: 'Database', original_id: int, original_channel: int) -> List[MirrorMessage]:
        """
        Finds `MirrorMessage` objects with `original_id` and `original_channel` values

        Args:
            original_id (`int`): Original message ID
            original_channel (`int`): Source channel ID

        Returns:
            List[MirrorMessage]
        """
        raise NotImplementedError