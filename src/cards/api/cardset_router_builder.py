from fastapi import APIRouter, Response

from .annotations import (
    RequesterIdAnnotation,
    OwnerIdAnnotation,
    OptionalCardsetIdAnnotation,
    OptionalUserIdAnnotation,
    OptionalOffsetAnnotation,
    OptionalLimitAnnotation,
    OptionalIncludeDeletedAnnotation,
    OptionalCardIdAnnotation,
    OptionalMixedAnnotation,
    CardsetSpecAnnotation,
    CardsetIdAnnotation,
    CardsetInfoSpecAnnotation,
    CardSpecAnnotation,
    CardIdAnnotation,
)

from .schemas import (
    CardsetInfoSchema,
    CardsetInfosSchema,
    CardSchema,
    CardsSchema,
    CardsStatus,
)

from ..core.cardset_service import CardsetService
from ..core.model import (
    CardsetInfo,
    CardsetInfoSpec,
    CardsetSpec,
    CardSpec,
    CardsStatus as CoreCardsStatus,
    Card,
)


class CardsetRouterBuilder:
    def __init__(self, cardset_service: CardsetService, *args, **kwargs):
        self.router = APIRouter(*args, **kwargs)
        self.cardset_service = cardset_service

        @self.router.get("/cardsets/", tags=["cardsets"])
        async def get_cardsets(
            requester_id: RequesterIdAnnotation,
            cardset_id: OptionalCardsetIdAnnotation = None,
            user_id: OptionalUserIdAnnotation = None,
            offset: OptionalOffsetAnnotation = 0,
            limit: OptionalLimitAnnotation = 10,
            include_deleted: OptionalIncludeDeletedAnnotation = False,
        ) -> Response:
            cardset_infos = self.cardset_service.get_cardset_infos(
                requester_id=requester_id,
                cardset_id=cardset_id,
                user_id=user_id,
                offset=offset,
                limit=limit,
                include_deleted=include_deleted,
            )

            cardset_infos_schema = CardsetInfosSchema(cardsets=[])
            for cardset_info in cardset_infos:
                cardset_infos_schema.cardsets.append(
                    CardsetInfoSchema(
                        title=cardset_info.title,
                        cardset_id=cardset_info.id,
                        description=cardset_info.description,
                        created_at=cardset_info.created_at,
                        modified_at=cardset_info.modified_at,
                        addressed_at=cardset_info.addressed_at,
                        status=CardsStatus(cardset_info.status),
                        owner_id=cardset_info.owner_id,
                    )
                )

            return Response(
                content=cardset_infos_schema.model_dump_json(),
                media_type="json",
                status_code=200,
            )

        @self.router.get("/cards/", tags=["cards"])
        async def get_cards(
            requester_id: RequesterIdAnnotation,
            card_id: OptionalCardIdAnnotation = None,
            cardset_id: OptionalCardsetIdAnnotation = None,
            offset: OptionalOffsetAnnotation = 0,
            limit: OptionalLimitAnnotation = 10,
            include_deleted: OptionalIncludeDeletedAnnotation = False,
            mixed: OptionalMixedAnnotation = False,
        ) -> Response:
            cards = self.cardset_service.get_cards(
                requester_id=requester_id,
                card_id=card_id,
                cardset_id=cardset_id,
                offset=offset,
                limit=limit,
                include_deleted=include_deleted,
                mixed=mixed,
            )

            cards_schema = CardsSchema(cards=[])
            for card in cards:
                cards_schema.cards.append(
                    CardSchema(
                        card_id=card.id,
                        cardset_id=card.cardset_id,
                        term=card.term,
                        description=card.description,
                        created_at=card.created_at,
                        modified_at=card.modified_at,
                        addressed_at=card.addressed_at,
                        status=CardsStatus(card.status),
                        owner_id=card.owner_id,
                    )
                )

            return Response(
                content=cards_schema.model_dump_json(),
                media_type="json",
                status_code=200,
            )

        @self.router.post("/cardsets/", tags=["cardsets"])
        async def create_cardset(
            requester_id: RequesterIdAnnotation,
            owner_id: OwnerIdAnnotation,
            spec: CardsetSpecAnnotation,
        ) -> Response:
            objects = []
            if spec.cards is not None:
                for card in spec.cards:
                    objects.append(
                        CardSpec(
                            term=card.term,
                            description=card.description,
                            status=CoreCardsStatus(card.status),
                        )
                    )

            cardset_spec = CardsetSpec(
                title=spec.title,
                description=spec.description,
                status=CoreCardsStatus(spec.status),
                cards=objects,
            )

            cardset_info: CardsetInfo | None = \
                self.cardset_service.create_cardset(
                    requester_id=requester_id,
                    owner_id=owner_id,
                    spec=cardset_spec,
                )

            if cardset_info is None:
                return Response(status_code=400)

            cardset_info_schema = CardsetInfoSchema(
                title=cardset_info.title,
                cardset_id=cardset_info.id,
                description=cardset_info.description,
                created_at=cardset_info.created_at,
                modified_at=cardset_info.modified_at,
                addressed_at=cardset_info.addressed_at,
                status=CardsStatus(cardset_info.status),
                owner_id=cardset_info.owner_id,
            )

            return Response(
                content=cardset_info_schema.model_dump_json(),
                media_type="json",
                status_code=201,
            )

        @self.router.patch("/cardset/{cardset_id}/", tags=["cardset"])
        async def modify_cardset(
            requester_id: RequesterIdAnnotation,
            cardset_id: CardsetIdAnnotation,
            spec: CardsetInfoSpecAnnotation,
        ) -> Response:
            cardset_info: CardsetInfo | None = \
                self.cardset_service.modify_cardset_info(
                    requester_id=requester_id,
                    cardset_id=cardset_id,
                    spec=CardsetInfoSpec(
                        title=spec.title,
                        description=spec.description,
                        status=CoreCardsStatus(spec.status),
                    ),
                )

            if cardset_info is None:
                return Response(status_code=400)

            cardset_info_schema = CardsetInfoSchema(
                title=cardset_info.title,
                cardset_id=cardset_info.id,
                description=cardset_info.description,
                created_at=cardset_info.created_at,
                modified_at=cardset_info.modified_at,
                addressed_at=cardset_info.addressed_at,
                status=CardsStatus(cardset_info.status),
                owner_id=cardset_info.owner_id,
            )

            return Response(
                content=cardset_info_schema.model_dump_json(),
                media_type="json",
                status_code=200,
            )

        @self.router.post("/cardset/{cardset_id}/cards/", tags=["cards"])
        async def create_card(
            requester_id: RequesterIdAnnotation,
            cardset_id: CardsetIdAnnotation,
            spec: CardSpecAnnotation,
        ) -> Response:
            card = self.cardset_service.create_card(
                requester_id=requester_id,
                cardset_id=cardset_id,
                spec=CardSpec(
                    term=spec.term,
                    description=spec.description,
                    status=CoreCardsStatus(spec.status),
                ),
            )

            if card is None:
                return Response(status_code=400)

            card_schema = CardSchema(
                card_id=card.id,
                cardset_id=card.cardset_id,
                term=card.term,
                description=card.description,
                created_at=card.created_at,
                modified_at=card.modified_at,
                addressed_at=card.addressed_at,
                status=CardsStatus(card.status),
                owner_id=card.owner_id,
            )
            return Response(
                content=card_schema.model_dump_json(),
                media_type="json",
                status_code=201,
            )

        @self.router.patch("/card/{card_id}/", tags=["card"])
        async def modify_card(
            requester_id: RequesterIdAnnotation,
            card_id: CardIdAnnotation,
            spec: CardSpecAnnotation,
        ) -> Response:
            card: Card | None = self.cardset_service.modify_card(
                requester_id=requester_id,
                card_id=card_id,
                spec=CardSpec(
                    term=spec.term,
                    description=spec.description,
                    status=CoreCardsStatus(spec.status),
                ),
            )

            if card is None:
                return Response(status_code=400)

            card_schema = CardSchema(
                card_id=card.id,
                cardset_id=card.cardset_id,
                term=card.term,
                description=card.description,
                created_at=card.created_at,
                modified_at=card.modified_at,
                addressed_at=card.addressed_at,
                status=CardsStatus(card.status),
                owner_id=card.owner_id,
            )

            return Response(
                content=card_schema.model_dump_json(),
                media_type="json",
                status_code=200,
            )
