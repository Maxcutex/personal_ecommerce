import enum

class Channels(str, enum.Enum):
    web = "web"
    slack = "slack"
    mobile = "mobile"

    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)


class OrderStatus(str, enum.Enum):
    booked = "booked"
    collected = "collected"
    cancelled = "cancelled"

    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)

