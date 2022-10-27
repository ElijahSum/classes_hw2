import json
import keyword
from collections import abc

json_dict = """{
    "title": "Iphone 10",
    "price": 100,
    "location": {
        "address": "город Москва, Лесная, 7",
        "metro_stations": ["Белорусская"]
        }
}"""


class ColorizeMixin:
    """ Добавляет цвет в print() """
    repr_color_code = 32  # default colour, can be changed in Advert

    def __str__(self):
        return f'\033[1;{self.repr_color_code}m {repr(self)}'


class Unpacker:
    """ Переделывает словарь в набор аттрибутов с соответствующим именем """

    def __init__(self, mapping):
        self._mapping = {}
        for key, val in mapping.items():
            if keyword.iskeyword(key):
                self._mapping[key + '_'] = val
            elif key == 'price':
                self._mapping['_' + key] = val
            else:
                self._mapping[key] = val

    def __getattr__(self, item):
        if hasattr(self._mapping, item):
            return getattr(self._mapping, item)
        else:
            if isinstance(self._mapping[item], abc.Mapping):
                return Unpacker(self._mapping[item])  # рекурсивно вызываем метод
            else:
                return self._mapping[item]


class Advert(ColorizeMixin, Unpacker):
    """ Осуществляем взаимодействие с json файлами """
    repr_color_code = 33

    def __init__(self, mapping):
        super().__init__(mapping)  # dynamically gets attributes via Unpacker
        self._price = self.price

    @property
    def price(self):
        try:
            self._price
        except:
            return 0
        else:
            if self._price < 0:
                raise ValueError('must be >= 0')
            else:
                return self._price

    def __repr__(self) -> str:
        return f'{self.title} | {self.price} ₽'


def main():
    test = json.loads(json_dict)
    test_class = Advert(test)
    print(test_class.__repr__())


if __name__ == "__main__":
    main()
