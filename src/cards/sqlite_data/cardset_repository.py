import sqlite3
import datetime
from typing import Optional, List
from ..core import CardsetRepositoryABC
from ..core import (
    Card,
    CardSpec,
    CardsetInfo,
    CardsetInfoSpec
)
from .utils import generate_unique_id
from .mappers import (
    CardMapper,
    CardsetInfoMapper,
    CardsStatusMapper
)


class CardsetRepository(CardsetRepositoryABC):
    def __init__(self, db_path: str):
        self.db_path = db_path

    def __execute_select_query(self, query, params=[]):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        print(query, params)
        cursor.execute(query, params)
        rows = cursor.fetchall()
        connection.close()
        return rows

    def __execute_insert_query(self, query, params=[]):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        conn.close()

    def get_cardset_infos(
        self,
        cardset_id: Optional[str] = None,
        user_id: Optional[str] = None,
        offset: Optional[int] = 0,
        limit: Optional[int] = 10,
        include_deleted: Optional[bool] = False,
    ) -> List[CardsetInfo]:
        """
            Метод get_cardset_infos возвращает наборы карточек в укороченном
            (без карточек) виде.
        """
        params = []

        where_causes = ""
        if cardset_id:
            where_causes += " AND id = ?"
            params.append(cardset_id)
        if user_id:
            where_causes += " AND owner_id = ?"
            params.append(user_id)
        if not include_deleted:
            where_causes += " AND status != ?"
            params.append('absent')

        query = f"""
            SELECT
                id, title, description, created_at, modified_at,
                addressed_at, status, owner_id
            FROM Cardset
            WHERE 1=1 {where_causes}
            ORDER BY title ASC
            LIMIT ? OFFSET ?
        """
        params.extend([str(limit), str(offset)])

        rows = self.__execute_select_query(query, params)
        return [CardsetInfoMapper.map(row) for row in rows]

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
        """
        query_parts = ["SELECT * FROM Card WHERE 1=1"]
        params = []

        if card_id:
            query_parts.append("AND id = ?")
            params.append(card_id)
        elif cardset_id:
            query_parts.append("AND cardset_id = ?")
            params.append(cardset_id)
        if not include_deleted:
            query_parts.append("AND status != ?")
            params.append("absent")

        order_clause = " ORDER BY term ASC"
        if not mixed:
            order_clause = " ORDER BY RANDOM()"

        query_parts.append(f"{order_clause} LIMIT ? OFFSET ?")
        params.extend([str(limit), str(offset)])
        query = ' '.join(query_parts)
        rows = self.__execute_select_query(query, params)
        return [CardMapper.map(row) for row in rows]

    def create_cardset_info(
        self,
        owner_id: str,
        spec: CardsetInfoSpec,
    ) -> CardsetInfo | None:
        """
            Метод create_cardset_info создает набор карточек (без карточек)
            с учетом переданных данных.
        """
        id = generate_unique_id(self.db_path, "Cardset", "id")
        inserted_datetime = datetime.datetime.now()
        title = spec.title if spec.title else ""
        description = spec.description if spec.description else ""
        status = "active"
        if spec.status:
            status = CardsStatusMapper.reverse_map(spec.status)

        query = """
            INSERT INTO Cardset (
                id, title, description, created_at, modified_at,
                addressed_at, status, owner_id
            ) VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?
            )
        """
        parameters = (
            id,
            title,
            description,
            inserted_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            inserted_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            inserted_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            status,
            owner_id
        )
        self.__execute_insert_query(query, parameters)

        return CardsetInfo(
            id=id,
            title=title,
            description=description,
            created_at=inserted_datetime,
            modified_at=inserted_datetime,
            addressed_at=inserted_datetime,
            status=CardsStatusMapper.map(status),
            owner_id=owner_id
        )

    def modify_cardset_info(
        self,
        cardset_id: str,
        spec: CardsetInfoSpec,
    ) -> CardsetInfo | None:
        """
            Метод modify_cardset изменяет набор карточек
            (карточки при этом не изменяются).
        """
        updated_datetime = datetime.datetime.now()

        old_infos = self.get_cardset_infos(cardset_id, include_deleted=True)
        if old_infos == []:
            return None
        old_info = old_infos[0]

        title = spec.title if spec.title else old_info.title
        description = old_info.description
        if spec.description:
            description = spec.description
        status = spec.status if spec.status else old_info.status

        query = """
            UPDATE Cardset SET
                title=?,
                description=?,
                status=?,
                modified_at=?
            WHERE id=?
        """
        params = [title, description, status, updated_datetime, cardset_id]
        self.__execute_insert_query(query, params)
        return self.get_cardset_infos(cardset_id, include_deleted=True)[0]

    def create_card(
        self,
        cardset_id: str,
        spec: CardSpec,
    ) -> Card | None:
        """
            Метод create_card создает карточку.
        """
        cardset = self.get_cardset_infos(cardset_id)[0]
        if not cardset:
            # TODO: сделать нормальное исключение
            raise Exception("Not valid cardset_id")

        new_card_id = generate_unique_id(self.db_path, "Card", "id")
        current_time = datetime.datetime.now()

        term = spec.term if spec.term else ""
        description = spec.description if spec.description else ""
        status = "active"
        if spec.status:
            status = CardsStatusMapper.reverse_map(spec.status)

        query = """
        INSERT INTO Card (
            id, term, description, created_at, modified_at,
            addressed_at, status, owner_id, cardset_id
        )
        VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?
        )
        """
        params = (
            new_card_id, term, description,
            current_time.strftime("%Y-%m-%d %H:%M:%S"),
            current_time.strftime("%Y-%m-%d %H:%M:%S"),
            current_time.strftime("%Y-%m-%d %H:%M:%S"),
            status, cardset.owner_id, cardset_id
        )

        self.__execute_insert_query(query, params)
        return Card(
            id=new_card_id,
            term=term,
            description=description,
            created_at=current_time,
            modified_at=current_time,
            addressed_at=current_time,
            status=CardsStatusMapper.map(status),
            owner_id=cardset.owner_id
        )

    def modify_card(
        self,
        card_id: str,
        spec: CardSpec,
    ) -> Card | None:
        """
        Метод modify_card изменяет карточку.
        """
        old_cards = self.get_cards(card_id, include_deleted=True)
        if old_cards == []:
            return None
        old_card = old_cards[0]

        params = [
            spec.term if spec.term else old_card.term,
            spec.description if spec.description else old_card.description,
            spec.status if spec.status else old_card.status,
            datetime.datetime.now(),
            card_id
        ]
        query = """
            UPDATE Card SET
                term = ?,
                description = ?,
                status = ?,
                modified_at = ?
            WHERE id = ?
        """
        self.__execute_insert_query(query, params)
        return self.get_cards(card_id, include_deleted=True)[0]
