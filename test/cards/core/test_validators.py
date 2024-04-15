from cards.core.validators import validate_id, validate_int
from cards import CardsInvalidArguments


def test_validate_id_true_positive():
    try:
        validate_id(
            id=None,
            required=True,
        )
    except CardsInvalidArguments:
        pass
    else:
        assert False, 'Exception expected, but no exception accured'


def test_validate_id_true_negative():
    try:
        validate_id(
            id=None,
            required=False,
        )
    except CardsInvalidArguments:
        assert False, 'No exception expected, but exception accured'


def test_validate_id_true_negative_valid_len():
    try:
        validate_id(
            id='aaaaaaaa',
            required=False,
        )
    except CardsInvalidArguments:
        assert False, 'No exception expected, but exception accured'


def test_validate_id_true_positive_invalid_len():
    try:
        validate_id(
            id='aaa',
            required=False,
        )
    except CardsInvalidArguments:
        pass
    else:
        assert False, 'Exception expected, but no exception accured'


def test_validate_int_true_positive():
    try:
        validate_int(
            val=None,
            required=True,
        )
    except CardsInvalidArguments:
        pass
    else:
        assert False, 'Exception expected, but no exception accured'
