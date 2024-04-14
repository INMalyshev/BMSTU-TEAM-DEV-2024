from pydantic import ValidationError

from cards.api.schemas import CardSpecSchema


def test_CardSpecSchema_valid_parametrs_works():
    external_data = {
        "term": "aaa",
        "description": "bbb",
        "status": "present",
    }

    try:
        CardSpecSchema(**external_data)
    except ValidationError as e:
        assert False, e.errors()


def test_CardSpecSchema_invalid_term_fails():
    external_data = {
        "term": "a" * 200,
        "description": "bbb",
        "status": "present",
    }

    try:
        CardSpecSchema(**external_data)
    except ValidationError as e:
        pass
    else:
        assert False, "Error expected."


def test_CardSpecSchema_invalid_description_fails():
    external_data = {
        "term": "aaa",
        "description": "a" * 513,
        "status": "present",
    }

    try:
        CardSpecSchema(**external_data)
    except ValidationError as e:
        pass
    else:
        assert False, "Error expected."


def test_CardSpecSchema_invalid_status_fails():
    external_data = {
        "term": "aaa",
        "description": "bbb",
        "status": "???",
    }

    try:
        CardSpecSchema(**external_data)
    except ValidationError as e:
        pass
    else:
        assert False, "Error expected."


def test_CardSpecSchema_None_values_works():
    external_data = {
        "term": None,
        "description": None,
        "status": None,
    }

    try:
        CardSpecSchema(**external_data)
    except ValidationError as e:
        assert False, e.errors()


def test_CardSpecSchema_enpty_data_works():
    external_data = {}

    try:
        CardSpecSchema(**external_data)
    except ValidationError as e:
        assert False, e.errors()
