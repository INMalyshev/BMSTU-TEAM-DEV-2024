from typing import Annotated

from fastapi import Query, Body, Path

from .schemas import (
    CardsetSpecSchema,
    CardsetInfoSpecSchema,
    CardSpecSchema,
)

from ..core.constants import ID_LENGTH, MAX_LIMIT


RequesterIdAnnotation = Annotated[str, Query(
    description="Идентификатор пользователя, \
        от имени которого выполняется действие.",
    pattern=r"^[a-zA-Z0-9]{" + rf"{ID_LENGTH}" + r"}$",
)]

OwnerIdAnnotation = Annotated[str, Query(
    description="Идентификатор пользователя - \
        владельца ресурса.",
)]

OptionalCardsetIdAnnotation = Annotated[str | None, Query(
    description="Уникальный идентификатор набора карточек.",
)]

CardsetIdAnnotation = Annotated[str, Path(
    description="Уникальный идентификатор набора карточек.",
)]

OptionalCardIdAnnotation = Annotated[str | None, Query(
    description="Уникальный идентификатор карточки.",
)]

CardIdAnnotation = Annotated[str, Path(
    description="Уникальный идентификатор карточки.",
)]

OptionalUserIdAnnotation = Annotated[str | None, Query(
    description="Уникальный идентификатор пользователя.",
)]

OptionalOffsetAnnotation = Annotated[int | None, Query(
    description="Смещение в рамках выборки.",
)]

OptionalLimitAnnotation = Annotated[int | None, Query(
    description="Максимальный размер выборки.",
    le=MAX_LIMIT,
)]

OptionalIncludeDeletedAnnotation = Annotated[bool | None, Query(
    description="Флаг возврата удаленных объектов.",
)]

OptionalMixedAnnotation = Annotated[bool | None, Query(
    description="Флаг возврата объектов в случайном порядке.",
)]

CardsetSpecAnnotation = Annotated[CardsetSpecSchema, Body(
    description="Информация о параметрах набора карточек.",
)]

CardsetInfoSpecAnnotation = Annotated[CardsetInfoSpecSchema, Body(
    description="Информация о параметрах набора карточек (без карточек).",
)]

CardSpecAnnotation = Annotated[CardSpecSchema, Body(
    description="Информация о параметрах карточки.",
)]
