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
        Метод get_cardset_infos возвращает наборы карточек
        в укороченном (без карточек) виде.

        Параметры
        ---
        requester_id: str
            id пользователя, от лица которого
            выполняется операция.
        cardset_id: str
            id набора кароточек. Если передано, остальные
            параметры не учитываются и возвращается
            только набор карточек с соответствующим
            id (если он существует).
        user_id: str
            id пользователя. Если передано, то вернутся
            наборы карточек, которые принадлежат
            пользователю с указанным id.
        offset, limit: int
            Параметры пагинации для результата.
        include_deleted: bool
            Если выставить данный параметр в True,
            в результирующей выборке могут оказаться
            наборы карточек, которые были отмечены
            как удаленные.

        Результат
        ---
        Возвращает выборку укороченных (без карточек)
        представлений наборов карточек. Результирующая
        выборка отсортирована по названию в алфавитном
        порядке.
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

        Параметры
        ---
        requester_id: str
            id пользователя, от лица которого выполняется
            операция.
        card_id: str
            id карточки. Если передано, остальные параметры
            игнорируются, а в результирующей
            выборке будет находиться объект с указанным
            id (если он существует).
        cardset_id: str
            id набора карточек. Если передано, то вернуться
            карточки, которые принадлежат
            набору карточек с переданным id (если они существуют).
        offset, limit: int
            Параметры пагинации для результата.
        include_deleted: bool
            Если выставить данный параметр в True, в результирующей
            выборке могут оказаться карточки, которые были отмечены
            как удаленные.
        mixed: bool
            Если выставить данный параметр в True, в результирующей
            выборке карточки будут представлены в случайном порядке.

        Результат
        ---
        Возвращает выборку карточек. Результирующая выборка
        отсортирована по термину в алфавитном порядке (если не
        выставлен параметр mixed).
        """
        raise NotImplementedError()

    @abstractmethod
    def create_cardset_info(
        self,
        owner_id: str,
        spec: CardsetInfoSpec,
    ) -> CardsetInfo | None:
        """
        Метод create_cardset_info создает набор карточек
        (без карточек) с учетом переданных данных.

        Параметры
        ---
        requester_id: str
            id пользователя, от лица которого
            выполняется операция.
        owner_id: str
            id создателя и владельца набора
            карточек и карточек внутри набора.
        spec: CardsetInfoSpec
            Перечень настраиваемых параметров
            набора карточек

        Результат
        ---
        В качестве результата успешного выполнения
        данного метода возвращается укороченное
        (без карточек) представление набора карточек.
        В случае, если создание набора карточек
        не было корректно выполнено, возвращается None.
        """
        raise NotImplementedError()

    @abstractmethod
    def modify_cardset_info(
        self,
        cardset_id: str,
        spec: CardsetInfoSpec,
    ) -> CardsetInfo | None:
        """
        Метод modify_cardset изменяет набор карточек
        (карточки при этом не изменяются).

        Параметры
        ---
        requester_id: str
            id пользователя, от лица которого
            выполняется операция.
        cardset_id: str
            id набора карточек для которого
            необходимо выполнить изменение.
        spec: CardsetMinimalSpec
            Перечень параметров набора карточек, которые
            должны быть изменены в рамках
            данной операции.

        Результат
        ---
        В качестве результата успешного выполнения
        данного метода возвращается укороченное
        (без карточек) представление набора карточек.
        В случае, если изменение набора карточек
        не было корректно выполнено, возвращается None.
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

        Параметры
        ---
        requester_id: str
            id пользователя, от лица которого
            выполняется операция.
        cardset_id: str
            id набора карточек в котором необходимо
            создать карточку.
        card_spec: CardSpec
            Перечень параметров карточки, которые должны
            быть изменены в рамках данной операции.

        Результат
        ---
        В качестве результата успешного выполнения
        данного метода возвращается карточка.
        В случае, если изменение карточки не было
        корректно выполнено, возвращается None.
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

        Параметры
        ---
        requester_id: str
            id пользователя, от лица которого
            выполняется операция.
        card_id: str
            id карточки для которой необходимо
            выполнить изменение.
        card_spec: CardSpec
            Перечень параметров карточки, которые
            должны быть изменены в рамках
            данной операции.

        Результат
        ---
        В качестве результата успешного выполнения
        данного метода возвращается карточка.
        В случае, если изменение карточки не было
        корректно выполнено, возвращается None.
        """
        raise NotImplementedError()
