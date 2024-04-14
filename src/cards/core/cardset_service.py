from typing import Optional, List

from .model import Card, CardsetInfo, CardsetSpec, CardsetInfoSpec, CardSpec
from .cardset_repository_abc import CardsetRepositoryABC
from .exceptions import CardsPermissionDenied, CardsInvalidArguments
from .validators import validate_id, validate_int
from .constants import MAX_LIMIT


class CardsetService:
    """
    CardsetService - класс для создания, управления
    и изменения наборов карточек и их содержимого.
    """

    def __init__(self, cardset_repository: CardsetRepositoryABC) -> None:
        self.cardset_repository = cardset_repository

    def get_cardset_infos(
        self,
        requester_id: str,
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
            id набора кароточек. Если передано,
            остальные параметры не учитываются и возвращается
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

        validate_id(requester_id, required=True)
        validate_id(cardset_id)
        validate_id(user_id)

        validate_int(offset, min_val=0)
        validate_int(limit, min_val=0, max_val=MAX_LIMIT)

        cardset_infos = self.cardset_repository.get_cardset_infos(
            cardset_id=cardset_id,
            user_id=user_id,
            offset=offset,
            limit=limit,
            include_deleted=include_deleted,
        )

        for cardset_info in cardset_infos:
            if cardset_info.owner_id != requester_id:
                raise CardsPermissionDenied(
                    "Неправомерный доступ к информации о наборах карточек"
                )

        return cardset_infos

    def get_cards(
        self,
        requester_id: str,
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
            id пользователя, от лица которого выполняется операция.
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
            Если выставить данный параметр в True, в
            результирующей выборке могут оказаться
            карточки, которые были отмечены как удаленные.
        mixed: bool
            Если выставить данный параметр в True, в
            результирующей выборке карточки будут
            представлены в случайном порядке.

        Результат
        ---
        Возвращает выборку карточек. Результирующая
        выборка отсортирована по термину в алфавитном
        порядке (если не выставлен параметр mixed).
        """

        validate_id(requester_id, required=True)
        validate_id(cardset_id)
        validate_id(card_id)

        validate_int(offset, min_val=0)
        validate_int(limit, min_val=0, max_val=MAX_LIMIT)

        cards = self.cardset_repository.get_cards(
            card_id=card_id,
            cardset_id=cardset_id,
            offset=offset,
            limit=limit,
            include_deleted=include_deleted,
            mixed=mixed,
        )

        for card in cards:
            if card.owner_id != requester_id:
                raise CardsPermissionDenied(
                    "Неправомерный доступ к информации о карточках"
                )

        return cards

    def create_cardset(
        self,
        requester_id: str,
        owner_id: str,
        spec: CardsetSpec,
    ) -> CardsetInfo | None:
        """
        Метод create_cardset создает набор карточек
        и наполняет его с учетом переданных данных.

        Параметры
        ---
        requester_id: str
            id пользователя, от лица которого
            выполняется операция.
        owner_id: str
            id создателя и владельца набора
            карточек и карточек внутри набора.
        spec: CardsetSpec
            Перечень настраиваемых параметров набора
            карточек, в том числе и самих карточек

        Результат
        ---
        В качестве результата успешного выполнения
        данного метода возвращается укороченное
        (без карточек) представление набора карточек.
        В случае, если создание набора карточек
        не было корректно выполнено, возвращается None.
        """
        validate_id(requester_id, required=True)
        validate_id(owner_id, required=True)

        cardset_info = self.cardset_repository.create_cardset_info(
            owner_id=owner_id,
            spec=CardsetInfoSpec(
                title=spec.title,
                description=spec.description,
                status=spec.status,
            ),
        )

        if cardset_info is None:
            return cardset_info

        if spec.cards is not None:
            for card_spec in spec.cards:
                card = self.cardset_repository.create_card(
                    cardset_id=cardset_info.id,
                    spec=card_spec,
                )

                if card is None:
                    return None

        return cardset_info

    def modify_cardset_info(
        self,
        requester_id: str,
        cardset_id: str,
        spec: CardsetInfoSpec,
    ) -> CardsetInfo | None:
        """
        Метод modify_cardset изменяет набор
        карточек (карточки при этом не изменяются).

        Параметры
        ---
        requester_id: str
            id пользователя, от лица которого
            выполняется операция.
        cardset_id: str
            id набора карточек для которого
            необходимо выполнить изменение.
        spec: CardsetMinimalSpec
            Перечень параметров набора карточек,
            которые должны быть изменены в рамках
            данной операции.

        Результат
        ---
        В качестве результата успешного выполнения
        данного метода возвращается укороченное
        (без карточек) представление набора карточек.
        В случае, если изменение набора карточек
        не было корректно выполнено, возвращается None.
        """

        validate_id(requester_id, required=True)
        validate_id(cardset_id, required=True)

        cardset_infos = self.cardset_repository.get_cardset_infos(
            cardset_id=cardset_id
        )
        if len(cardset_infos) < 1:
            raise CardsInvalidArguments(
                f"Набора карточек {cardset_id} не обнаружено."
            )
        if cardset_infos[0].owner_id != requester_id:
            raise CardsPermissionDenied(
                "Неправомерный доступ к информации о наборах карточек"
            )

        cardset_info = self.cardset_repository.modify_cardset_info(
            cardset_id=cardset_id,
            spec=spec,
        )

        return cardset_info

    def create_card(
        self,
        requester_id: str,
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
            id набора карточек в котором
            необходимо создать карточку.
        card_spec: CardSpec
            Перечень параметров карточки,
            которые должны быть изменены в рамках
            данной операции.

        Результат
        ---
        В качестве результата успешного выполнения
        данного метода возвращается карточка.
        В случае, если изменение карточки не было
        корректно выполнено, возвращается None.
        """

        validate_id(requester_id, required=True)
        validate_id(cardset_id, required=True)

        cardset_infos = self.cardset_repository.get_cardset_infos(
            cardset_id=cardset_id
        )
        if len(cardset_infos) < 1:
            raise CardsInvalidArguments(
                f"Набора карточек {cardset_id} не обнаружено."
            )
        if cardset_infos[0].owner_id != requester_id:
            raise CardsPermissionDenied(
                "Неправомерный доступ к информации о наборах карточек"
            )

        card = self.cardset_repository.create_card(
            cardset_id=cardset_id,
            spec=spec,
        )

        return card

    def modify_card(
        self,
        requester_id: str,
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

        validate_id(requester_id, required=True)
        validate_id(card_id, required=True)

        cards = self.cardset_repository.get_cards(card_id=card_id)
        if len(cards) < 1:
            raise CardsInvalidArguments(f"Карточки {cards} не обнаружено.")
        if cards[0].owner_id != requester_id:
            raise CardsPermissionDenied(
                "Неправомерный доступ к информации о карточках"
            )

        card = self.cardset_repository.modify_card(
            card_id=card_id,
            spec=spec,
        )

        return card
