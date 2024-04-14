from abc import ABC, abstractmethod
from ..core import (
    Card,
    CardsetInfo,
    CardsStatus
)


class BaseMapper(ABC):
    @abstractmethod
    def map(row):
        """
        Метод для конвертации строки, полученной из sqlite в нужный объект
        """
        raise NotImplementedError()


class CardsStatusMapper(BaseMapper):
    @staticmethod
    def map(row):
        if row == 'present':
            return CardsStatus.PRESENT
        if row == 'absent':
            return CardsStatus.ABSENT

        # TODO: завести исключение под неправильный статус
        raise Exception()

    @staticmethod
    def reverse_map(card_status):
        if card_status == CardsStatus.ABSENT:
            return 'absent'
        if card_status == CardsStatus.PRESENT:
            return 'present'

        # TODO: завести исключение под неправильный статус
        raise Exception()


class CardsetInfoMapper(BaseMapper):
    @staticmethod
    def map(row):
        return CardsetInfo(
            id=row[0],
            title=row[1],
            description=row[2],
            created_at=row[3],
            modified_at=row[4],
            addressed_at=row[5],
            status=CardsStatusMapper.map(row[6]),
            owner_id=row[7]
        )


class CardMapper(BaseMapper):
    @staticmethod
    def map(row):
        return Card(
            id=row[0],
            term=row[1],
            description=row[2],
            created_at=row[3],
            modified_at=row[4],
            addressed_at=row[5],
            status=CardsStatusMapper.map(row[6]),
            owner_id=row[7],
            cardset_id=row[8],
        )
