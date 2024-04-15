from typing import Optional

from .constants import ID_LENGTH
from .exceptions import CardsInvalidArguments


def validate_id(id: Optional[str] = None, required: bool = False) -> None:
    if id is None:
        if required:
            raise CardsInvalidArguments("Идентификатор не был передан.")
        return
    if len(id) != ID_LENGTH:
        raise CardsInvalidArguments(
            f"Неправильный id: ожидалось {ID_LENGTH}, получено {len(id)}."
        )


def validate_int(
    val: Optional[int] = None,
    min_val: Optional[int] = None,
    max_val: Optional[int] = None,
    required: bool = False,
) -> None:
    if val is None:
        if required:
            raise CardsInvalidArguments("Параметр не был передан.")
        return
    if min_val is not None and val < min_val:
        raise CardsInvalidArguments(
            f"Недопустимое значение {val}: меньше минимума {min_val}."
        )
    if max_val is not None and val > max_val:
        raise CardsInvalidArguments(
            f"Недопустимое значение {val}: больше максимума {max_val}."
        )
