""" Advert class """
import json
from keyword import iskeyword
from collections import namedtuple


class ColorizeMixin:
    """
    Mixin for colorizing advertisement info
    """

    def __repr__(self):
        color_code = self.repr_color_code
        repr_str = super().__repr__()
        return f"\033[1:{color_code}:48m{repr_str}\033[00m"

    def func(self):
        """
        Fictitious method to pass Pylint refactor problem
        :return: None
        """


class JSONParser:
    """
    Set fields to object from dict
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

    def func(self):
        """
        Fictitious method to pass Pylint refactor problem
        :return: None
        """


class BaseAdvert:
    """
    Stores information about advertisement
    """

    def __init__(self, json_dict: dict):
        dict_parser = JSONParser()
        dict_parser(self, json_dict)
        self._check_title()

    def _check_title(self) -> None:
        if not hasattr(self, 'title'):
            raise ValueError("advertisement doesn't have field 'title'")

    def _check_price(self, price=None) -> None:
        price = self._price if price is None else price

        if not isinstance(price, int):
            raise ValueError(f"type(price) = {type(self.price)}, should be int")

        if price < 0:
            raise ValueError("must be >= 0")

    @property
    def price(self) -> int:
        """
        Price in the advertisement
        :return price: int
        """
        return self._price

    @price.setter
    def price(self, value):
        self._check_price(value)
        self._price = value

    def __repr__(self):
        return f"{getattr(self, 'title')} | {self.price} ₽"


class Advert(ColorizeMixin, BaseAdvert):
    """
    Advertisement with colorized text
    """

    def __init__(self, json_dict: dict):
        BaseAdvert.__init__(self, json_dict)
        ColorizeMixin.__init__(self)

    def func(self):
        """
        Fictitious method to pass Pylint refactor problem
        :return: None
        """


if __name__ == '__main__':
    LESSON_STR = """{
        "title": "python",
        "price": 0,
        "location": {
            "address": "город Москва, Лесная, 7",
            "metro_stations": ["Белорусская"]
        }
    }"""
    CORGI_STR = """{
        "title": "Вельш-корги",
        "price": 1000,
        "class": "dogs",
        "location": {
            "address": "сельское поселение Ельдигинское, \
                поселок санатория Тишково, 25"
        },
        "repr_color_code": 32
    }"""
    IPHONE_STR = """{
        "title": "iPhone X",
        "price": -100,
        "location": {
            "address": "город Самара, улица Мориса Тореза, 50",
            "metro_stations": ["Спортивная", "Гагаринская"]
        }
    }"""

    lesson = json.loads(LESSON_STR)
    corgi = json.loads(CORGI_STR)
    iphone = json.loads(IPHONE_STR)

    lesson_ad = BaseAdvert(lesson)
    corgi_ad = Advert(corgi)
    iphone_ad = BaseAdvert(iphone)

    print(lesson_ad)
    print(lesson_ad.location.address)

    print(corgi_ad)
    print(corgi_ad.class_)

    print(iphone_ad)
    print(iphone_ad.price)

    try:
        iphone_ad.price = -1
    except ValueError:
        print("Negative price wasn't set!")

    try:
        BAD_IPHONE_STR = """{
            "title": "iPhone X",
            "price": -1
        }"""
        bad_iphone = json.loads(BAD_IPHONE_STR)
        bad_iphone_ad = BaseAdvert(bad_iphone)
    except ValueError as err:
        print("Incorrect advertisement wasn't created!")
