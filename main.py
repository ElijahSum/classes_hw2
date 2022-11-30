import json
from keyword import iskeyword
from collections import namedtuple

json_dict = """{
    "title": "Iphone 10",
    "price": 100,
    "location": {
        "address": "город Москва, Лесная, 7",
        "metro_stations": ["Белорусская"]
        }
}"""


class ColorizeMixin:
    """
    Добавляет цвет в repr или str
    """
    repr_color_code = 33  # default colour, can be changed in Advert

    def __repr__(self):
        color_code = self.repr_color_code
        repr_str = super().__repr__()
        return f"\033[1:{color_code}:48m{repr_str}\033[00m"


class Unpacker:
    """
    Переделывает словарь в набор аттрибутов с соответствующим именем
    """

    def __call__(self, obj: object, dct: dict) -> None:
        for key, val in dct.items():
            if iskeyword(key):
                key += '_'

            if isinstance(val, dict):
                key_type = namedtuple(f'{key}', val.keys())
                setattr(obj, key, key_type(**val))
                self.__call__(getattr(obj, key), val)
            elif not hasattr(obj, key):
                setattr(obj, key, val)


class BaseAdvert:
    """
    Содержит всю информацию об объявлении
    """

    def __init__(self, mapping: dict):
        dict_parser = Unpacker()
        dict_parser(self, mapping)
        self._check_title()

    def _check_title(self) -> None:
        if not hasattr(self, 'title'):
            raise ValueError("advertisement doesn't have field 'title'")

    def _check_price(self, price=None) -> None:
        price = self._price if price is None else price

        if not isinstance(price, int):
            raise ValueError(f"Тип price - {type(self.price)}, ожидалось int")

        if price < 0:
            raise ValueError("must be >= 0")

    @property
    def price(self) -> int:
        return self._price

    @price.setter
    def price(self, value):
        self._check_price(value)
        self._price = value

    def __repr__(self):
        return f"{getattr(self, 'title')} | {self.price} ₽"


class Advert(ColorizeMixin, BaseAdvert):
    """
    Совмещает два родительских класса - делает цветной вывод
    """

    def __init__(self, mapping: dict):
        BaseAdvert.__init__(self, mapping)
        ColorizeMixin.__init__(self)


def main():
    test = json.loads(json_dict)
    test_class = Advert(test)
    print(test_class.__str__())
    print(test_class.__dict__)


if __name__ == "__main__":
    main()
