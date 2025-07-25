from exceptions import MethodValidationException, DateSearchValidationException, CityValidationException
from datetime import datetime, date
import re

class MethodValidator:
    @classmethod
    def validate(cls, current_method: str, correct_method: str):
        if current_method != correct_method:
            raise MethodValidationException(f'Необходимо использовать метод {correct_method}', code=11555)

class DateSearchValidator:
    @classmethod
    def validate(cls, check_in: str, check_out: str):

        if check_in is None or check_out is None:
            raise DateSearchValidationException("Дата заезда и дата выезда обязательны для заполнения", code=11005)
        if check_in is None:
            raise DateSearchValidationException("Дата заезда обязательна для заполнения", code=11006)
        if check_out is None:
            raise DateSearchValidationException("Дата выезда обязательна для заполнения", code=11007)

        try:
            check_in_date = datetime.strptime(check_in, "%Y-%m-%d").date()
            check_out_date = datetime.strptime(check_out, "%Y-%m-%d").date()
        except ValueError:
            raise DateSearchValidationException("Неверный формат даты", code=11011)


        if check_in_date > check_out_date:
            raise DateSearchValidationException("Дата заезда не может быть позже даты выезда", code=11008)
        if check_out_date < check_in_date:
            raise DateSearchValidationException("Дата выезда не может быть раньше даты заезда", code=11009)
        if check_in_date < date.today():
            raise DateSearchValidationException("Дата заезда не может быть меньше текущей даты", code=11010)
        if check_in_date == check_out:
            raise DateSearchValidationException("Дата заезда не может совпадать с датой выезда", code=11011)

class CityValidator:
    valid_cities = {"Москва", "Санкт-Петербург"}

    @classmethod
    def validate(cls, city: str):
        if city is None:
            raise CityValidationException("Параметр city обязателен для передачи", code=11003)
        if not city.strip() and city is not None:
            raise CityValidationException("Параметр city не может быть пустым", code=11001)
        if not re.fullmatch(r"[A-Za-zА-Яа-яЁё\-]+", city):
            raise CityValidationException("City может содержать только латиницу, кириллицу и дефис", code=11004)
        if city not in cls.valid_cities:
            raise CityValidationException("В указанном городе нет свободных отелей", code=11002)