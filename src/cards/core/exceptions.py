class CardsException(Exception):
    """Базовое исключение модуля cards."""


class CardsPermissionDenied(CardsException):
    """
    Исключение модуля cards связанное с попыткой неправомерного
    обращения к объектам системы.
    """


class CardsInvalidArguments(CardsException):
    """
    Исключение модуля cards связанное с попыткой передачи
    некорректных данных при вызове методов модуля.
    """
