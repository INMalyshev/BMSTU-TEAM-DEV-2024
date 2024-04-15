from abc import ABC, abstractmethod
from typing import Optional, List
from .model import Card, CardsetInfo, CardsetInfoSpec, CardSpec


class CardsetRepositoryABC(ABC):
    @abstractmethod
    def get_cardset_infos(
        self,
        cardset_id: Optional[str] = None,
        user_id: Optional[str] = None,
        offset: Optional[int] = 0,
        limit: Optional[int] = 10,
        include_deleted: Optional[bool] = False,
    ) -> List[CardsetInfo]:
        """
        Возвращает наборы карточек в укороченном (без карточек) виде.

        :param cardset_id: ID набора карточек. Если передано, остальные
        параметры не учитываются и возвращается только набор карточек с
        соответствующим ID (если он существует).
        :type cardset_id: str, optional
        :param user_id: ID пользователя. Если передано, то вернутся наборы
        карточек, которые принадлежат пользователю с указанным ID.
        :type user_id: str, optional
        :param offset: Параметр пагинации для результата, указывает с какой
        записи начинать выборку.
        :type offset: int, optional
        :param limit: Параметр пагинации для результата, указывает
        максимальное количество записей в выборке.
        :type limit: int, optional
        :param include_deleted: Если True, в результирующей выборке могут
        оказаться наборы карточек, которые были отмечены как удаленные.
        :type include_deleted: bool, optional
        :return: Выборка укороченных (без карточек) представлений наборов
        карточек, отсортированная по названию в алфавитном порядке.
        :rtype: List[CardsetInfo]
        """
        raise NotImplementedError()

    @abstractmethod
    def get_cards(
        self,
        card_id: Optional[str] = None,
        cardset_id: Optional[str] = None,
        offset: Optional[int] = 0,
        limit: Optional[int] = 10,
        include_deleted: Optional[bool] = False,
        mixed: Optional[bool] = False,
    ) -> List[Card]:
        """
        Метод get_cards возвращает выборку карточек.

        :param card_id: id карточки. Если передано, остальные параметры
        игнорируются, а в результирующей выборке будет находиться объект
        с указанным id (если он существует).
        :type card_id: Optional[str], optional
        :param cardset_id: id набора карточек. Если передано, то вернуться
        карточки, которые принадлежат набору карточек с переданным id
        (если они существуют).
        :type cardset_id: Optional[str], optional
        :param offset: Параметр пагинации для результата.
        :type offset: Optional[int], optional
        :param limit: Параметр пагинации для результата.
        :type limit: Optional[int], optional
        :param include_deleted: Если выставить данный параметр в True,
        в результирующей выборке могут оказаться карточки, которые были
        отмечены как удаленные.
        :type include_deleted: Optional[bool], optional
        :param mixed: Если выставить данный параметр в True, в
        результирующей выборке карточки будут представлены в случайном
        порядке.
        :type mixed: Optional[bool], optional
        :return: Возвращает выборку карточек. Результирующая выборка
        отсортирована по термину в алфавитном порядке (если не выставлен
        параметр mixed).
        :rtype: List[Card]
        """
        raise NotImplementedError()

    @abstractmethod
    def create_cardset_info(
        self,
        owner_id: str,
        spec: CardsetInfoSpec,
    ) -> CardsetInfo | None:
        """
        Метод create_cardset_info создает набор карточек (без карточек)
        с учетом переданных данных.

        :param owner_id: id создателя и владельца набора карточек и
        карточек внутри набора.
        :type owner_id: str
        :param spec: Перечень настраиваемых параметров набора карточек.
        :type spec: CardsetInfoSpec
        :return: Укороченное (без карточек) представление набора
        карточек или None, если создание набора карточек не было
        корректно выполнено.
        :rtype: CardsetInfo | None
        """
        raise NotImplementedError()

    @abstractmethod
    def modify_cardset_info(
        self,
        cardset_id: str,
        spec: CardsetInfoSpec,
    ) -> CardsetInfo | None:
        """
        Метод modify_cardset изменяет набор карточек (карточки при этом
        не изменяются).

        :param cardset_id: id набора карточек для которого необходимо
        выполнить изменение.
        :type cardset_id: str
        :param spec: Перечень параметров набора карточек, которые должны
        быть изменены в рамках данной операции.
        :type spec: CardsetInfoSpec
        :return: Укороченное (без карточек) представление набора карточек
        или None, если изменение набора карточек не было корректно выполнено.
        :rtype: CardsetInfo | None
        """
        raise NotImplementedError()

    @abstractmethod
    def create_card(
        self,
        cardset_id: str,
        spec: CardSpec,
    ) -> Card | None:
        """
        Метод create_card создает карточку.

        :param cardset_id: id набора карточек, в котором необходимо
        создать карточку.
        :type cardset_id: str
        :param spec: Перечень параметров карточки, которые должны
        быть изменены в рамках данной операции.
        :type spec: CardSpec

        :return: В качестве результата успешного выполнения данного метода
        возвращается карточка. В случае, если изменение карточки не было
        корректно выполнено, возвращается None.
        :rtype: Card | None
        """
        raise NotImplementedError()

    @abstractmethod
    def modify_card(
        self,
        card_id: str,
        spec: CardSpec,
    ) -> Card | None:
        """
        Метод modify_card изменяет карточку.

        :param card_id: id карточки, для которой необходимо выполнить
        изменение.
        :type card_id: str
        :param spec: Перечень параметров карточки, которые должны быть
        изменены в рамках данной операции.
        :type spec: CardSpec

        :return: В качестве результата успешного выполнения данного метода
        возвращается карточка. В случае, если изменение карточки не было
        корректно выполнено, возвращается None.
        :rtype: Card | None
        """
        raise NotImplementedError()
