from cards import (
    SqliteDbHandler,
    CardsetRepository,
    CardsetInfoSpec,
    CardsStatus,
    CardSpec
)

db_path = 'test_database.db'


def test_create_all_tables():
    db_hander = SqliteDbHandler(db_path)
    db_hander.initialize_db()

    expected_tables = ['CardsStatus', 'Cardset', 'Card']
    real_tables = db_hander.list_tables()

    assert set(expected_tables) == set(real_tables)
    db_hander.delete_database_file()


def test_create_cardset_info():
    db_hander = SqliteDbHandler(db_path)
    db_hander.initialize_db()

    repo = CardsetRepository(db_path)
    cardset_info = repo.create_cardset_info(
        "cuteseal",
        CardsetInfoSpec("title", "description", CardsStatus.PRESENT)
    )

    assert cardset_info.title == "title"
    assert cardset_info.description == "description"
    assert cardset_info.status == CardsStatus.PRESENT
    assert cardset_info.owner_id == "cuteseal"

    db_hander.delete_database_file()


def test_get_cardset_info():
    db_hander = SqliteDbHandler(db_path)
    db_hander.initialize_db()

    repo = CardsetRepository(db_path)
    cardset_that_was_create = repo.create_cardset_info(
        "cuteseal",
        CardsetInfoSpec("title", "description", CardsStatus.PRESENT)
    )
    cardset_that_was_get = repo.get_cardset_infos(
        cardset_that_was_create.id
    )[0]

    assert cardset_that_was_get.title == "title"
    assert cardset_that_was_get.description == "description"
    assert cardset_that_was_get.status == CardsStatus.PRESENT
    assert cardset_that_was_get.owner_id == "cuteseal"

    db_hander.delete_database_file()


def test_create_card():
    db_hander = SqliteDbHandler(db_path)
    db_hander.initialize_db()

    repo = CardsetRepository(db_path)
    cardset = repo.create_cardset_info(
        "cuteseal",
        CardsetInfoSpec("title", "description", CardsStatus.PRESENT)
    )
    card = repo.create_card(
        cardset.id,
        CardSpec("term", "description", CardsStatus.PRESENT)
    )

    assert card.term == "term"
    assert card.description == "description"
    assert card.status == CardsStatus.PRESENT
    assert card.owner_id == "cuteseal"

    db_hander.delete_database_file()


def test_get_card():
    db_hander = SqliteDbHandler(db_path)
    db_hander.initialize_db()

    repo = CardsetRepository(db_path)
    cardset = repo.create_cardset_info(
        "cuteseal",
        CardsetInfoSpec("title", "description", CardsStatus.PRESENT)
    )
    card_that_was_create = repo.create_card(
        cardset.id,
        CardSpec("term", "description", CardsStatus.PRESENT)
    )
    card_that_was_get = repo.get_cards(
        card_that_was_create.id
    )[0]

    assert card_that_was_get.term == "term"
    assert card_that_was_get.description == "description"
    assert card_that_was_get.status == CardsStatus.PRESENT
    assert card_that_was_get.owner_id == "cuteseal"

    db_hander.delete_database_file()


def test_modify_cardset():
    db_hander = SqliteDbHandler(db_path)
    db_hander.initialize_db()

    repo = CardsetRepository(db_path)
    cardset = repo.create_cardset_info(
        "cuteseal",
        CardsetInfoSpec("title", "description", CardsStatus.PRESENT)
    )
    new_cardset = repo.modify_cardset_info(
        cardset.id,
        CardsetInfoSpec("title1", "description1", CardsStatus.ABSENT)
    )

    assert new_cardset.title == "title1"
    assert new_cardset.description == "description1"
    assert new_cardset.status == CardsStatus.ABSENT
    assert new_cardset.owner_id == "cuteseal"

    db_hander.delete_database_file()


def test_modify_card():
    db_hander = SqliteDbHandler(db_path)
    db_hander.initialize_db()

    repo = CardsetRepository(db_path)
    cardset = repo.create_cardset_info(
        "cuteseal",
        CardsetInfoSpec("title", "description", CardsStatus.PRESENT)
    )
    card_that_was_create = repo.create_card(
        cardset.id,
        CardSpec("term", "description", CardsStatus.PRESENT)
    )
    card_that_was_get = repo.modify_card(
        card_that_was_create.id,
        CardSpec("term1", "description1", CardsStatus.ABSENT)
    )

    assert card_that_was_get.term == "term1"
    assert card_that_was_get.description == "description1"
    assert card_that_was_get.status == CardsStatus.ABSENT
    assert card_that_was_get.owner_id == "cuteseal"

    db_hander.delete_database_file()
