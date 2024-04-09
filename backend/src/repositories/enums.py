from enum import Enum


class BaseEnum(str, Enum):
    def __str__(self) -> str:
        return str.__str__(self)


class OrderEnum:
    ASC = "asc"
    DESC = "desc"


class SortEnum:
    CREATED_AT = "create_at"
