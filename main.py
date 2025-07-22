from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime, date
from typing import Optional, List
import re


app = FastAPI()


class CityValidationException(Exception):
    def __init__(self, message: str, code: int = 11000):
        self.message = message
        self.code = code
        super().__init__(message)

class DateSearchValidationException(Exception):
    def __init__(self, message: str, code: int = 11000):
        self.message = message
        self.code = code
        super().__init__(message)

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





class Hotel:
    def __init__(self, id: int, hotel_name: str, description: str, city: str, country: str, stars: Optional[int], price: float):
        self.id = id
        self.hotel_name = hotel_name
        self.description = description
        self.city = city
        self.country = country
        self.stars = stars
        self.price = price

    def to_dict(self):
        return {
            "id": self.id,
            "hotel_name": self.hotel_name,
            "description": self.description,
            "city": self.city,
            "country": self.country,
            "stars": self.stars,
            "price": self.price,
        }




class HotelSearchService:
    def __init__(self, city: str, check_in: Optional[date], check_out: Optional[date]):
        self.city = city
        self.check_in = check_in
        self.check_out = check_out

    def search(self):
        CityValidator.validate(self.city)
        DateSearchValidator.validate(self.check_in, self.check_out)

        # Пример отелей
        hotels = [
            Hotel(1, "Невский Берег #1", "Историческое здание и высокий сервис", "Москва", "Russia", 4, 3296),
            Hotel(2, "Сити Хаус #2", "Уютный номер и вид на парк", "Санкт-Петербург", "Russia", 5, 4014),
            Hotel(3, "Fontanka Inn #3", "Рядом с метро и музеями", "Санкт-Петербург", "Russia", None, 2713),
            Hotel(4, "Московский Мост #4", "Уютный номер и вид на парк", "Москва", "Russia", 5, 3895),
            Hotel(5, "Vintage Inn #5", "Для деловых поездок и семейного отдыха", "Санкт-Петербург", "Russia", None,
                  2922),
            Hotel(6, "Кутузов Палас #6", "Историческое здание и высокий сервис", "Москва", "Russia", 5, 3692),
            Hotel(7, "Nevsky Boutique #7", "Рядом с метро и музеями", "Москва", "Russia", 2, 4059),
            Hotel(8, "Lite Garden #8", "Современный отель у набережной", "Санкт-Петербург", "Russia", None, 1484),
            Hotel(9, "Гранд Отель Москва #9", "Современный отель у набережной", "Санкт-Петербург", "Russia", 2, 4260),
            Hotel(10, "Royal Moscow #10", "Тихое место с панорамным видом", "Москва", "Russia", 3, 4256),
            Hotel(11, "Sokolniki Inn #11", "Рядом с метро и музеями", "Москва", "Russia", 4, 4116),
            Hotel(12, "Vintage Inn #12", "Комфорт и роскошь в центре города", "Санкт-Петербург", "Russia", None, 3281),
            Hotel(13, "Sunny Place #13", "Комфорт и роскошь в центре города", "Москва", "Russia", 4, 4692),
            Hotel(14, "Golden Garden #14", "Апартаменты с кухней", "Санкт-Петербург", "Russia", 5, 3082),
            Hotel(15, "Галерея Отель #15", "Комфорт и роскошь в центре города", "Санкт-Петербург", "Russia", 4, 1380),
            Hotel(16, "Мост Отель #16", "Комфорт и роскошь в центре города", "Москва", "Russia", 4, 1875),
            Hotel(17, "Hermitage Suites #17", "Уютный номер и вид на парк", "Москва", "Russia", 3, 1483),
            Hotel(18, "Urban Star #18", "Современный отель у набережной", "Москва", "Russia", 2, 1876),
            Hotel(19, "Hermitage Suites #19", "Рядом с метро и музеями", "Москва", "Russia", None, 2031),
            Hotel(20, "Golden Garden #20", "Современный отель у набережной", "Москва", "Russia", 3, 4172),
            Hotel(21, "Old Town Stay #21", "Современный отель у набережной", "Санкт-Петербург", "Russia", 4, 4236),
            Hotel(22, "Capital Suites #22", "Апартаменты с кухней", "Москва", "Russia", 2, 3105),
            Hotel(23, "River View Hotel #23", "Просторные номера и ресторан", "Москва", "Russia", 5, 3848),
            Hotel(24, "Sunny Place #24", "Бюджетный отель с качественным сервисом", "Санкт-Петербург", "Russia", 4,
                  4440),
            Hotel(25, "City Comfort #25", "Историческое здание и высокий сервис", "Санкт-Петербург", "Russia", 4, 2001),
            Hotel(26, "Aurora Palace #26", "Апартаменты с кухней", "Москва", "Russia", 5, 1073),
            Hotel(27, "Невский Берег #27", "Уютный номер и вид на парк", "Санкт-Петербург", "Russia", 3, 3184),
            Hotel(28, "Тверская Премьер #28", "Рядом с метро и музеями", "Москва", "Russia", 5, 1881),
            Hotel(29, "Golden Garden #29", "Историческое здание и высокий сервис", "Москва", "Russia", 4, 4649),
            Hotel(30, "Сити Хаус #30", "Рядом с метро и музеями", "Москва", "Russia", 2, 2233),
            Hotel(31, "Northern Lights #31", "Историческое здание и высокий сервис", "Москва", "Russia", 2, 1684),
            Hotel(32, "Golden Garden #32", "Для деловых поездок и семейного отдыха", "Москва", "Russia", 3, 3714),
            Hotel(33, "Urban Star #33", "Современный отель у набережной", "Санкт-Петербург", "Russia", 4, 2255),
            Hotel(34, "Невский Берег #34", "Комфорт и роскошь в центре города", "Санкт-Петербург", "Russia", None, 1318),
            Hotel(35, "Парк Премьер #35", "Современный отель у набережной", "Москва", "Russia", 2, 2791),
            Hotel(36, "City Comfort #36", "Просторные номера и ресторан", "Санкт-Петербург", "Russia", 4, 2033),
            Hotel(37, "Отель Метрополь #37", "Комфорт и роскошь в центре города", "Москва", "Russia", 3, 2383),
            Hotel(38, "Fontanka Light #38", "Историческое здание и высокий сервис", "Санкт-Петербург", "Russia", 5,
                  2414),
            Hotel(39, "Heritage Place #39", "Бюджетный отель с качественным сервисом", "Санкт-Петербург", "Russia", 5,
                  3301),
            Hotel(40, "Hermitage Suites #40", "Современный отель у набережной", "Москва", "Russia", 4, 4074),
            Hotel(41, "Palace Line #41", "Уютный номер и вид на парк", "Москва", "Russia", None, 4152),
            Hotel(42, "Palace Line #42", "Просторные номера и ресторан", "Санкт-Петербург", "Russia", None, 4687),
            Hotel(43, "Fontanka Light #43", "Историческое здание и высокий сервис", "Москва", "Russia", 5, 3939),
            Hotel(44, "Palace Line #44", "Апартаменты с кухней", "Санкт-Петербург", "Russia", 5, 4672),
            Hotel(45, "Sokolniki Inn #45", "Тихое место с панорамным видом", "Санкт-Петербург", "Russia", 3, 4362),
            Hotel(46, "River View Hotel #46", "Историческое здание и высокий сервис", "Москва", "Russia", 4, 3676),
            Hotel(47, "Heritage Place #47", "Историческое здание и высокий сервис", "Москва", "Russia", 4, 4868),
            Hotel(48, "SkyLine Plaza #48", "Тихое место с панорамным видом", "Санкт-Петербург", "Russia", 5, 1904),
            Hotel(49, "Zamoskvorechye Classic #49", "Для деловых поездок и семейного отдыха", "Москва", "Russia", None,
                  3931),
            Hotel(50, "Art Hotel #50", "Для деловых поездок и семейного отдыха", "Москва", "Russia", 4, 1539),
            Hotel(51, "Royal Moscow #51", "Тихое место с панорамным видом", "Санкт-Петербург", "Russia", 3, 4323),
            Hotel(52, "Hermitage Suites #52", "Тихое место с панорамным видом", "Санкт-Петербург", "Russia", 2, 1244),
            Hotel(53, "Sunny Place #53", "Рядом с метро и музеями", "Санкт-Петербург", "Russia", 3, 1702),
            Hotel(54, "Botanic Residence #54", "Тихое место с панорамным видом", "Москва", "Russia", None, 3905),
            Hotel(55, "Art Hotel #55", "Современный отель у набережной", "Санкт-Петербург", "Russia", 5, 4628),
            Hotel(56, "River View Hotel #56", "Для деловых поездок и семейного отдыха", "Санкт-Петербург", "Russia", 4,
                  4679),
            Hotel(57, "Sokolniki Inn #57", "Комфорт и роскошь в центре города", "Москва", "Russia", 3, 1915),
            Hotel(58, "Urban Star #58", "Просторные номера и ресторан", "Санкт-Петербург", "Russia", 3, 1028),
            Hotel(59, "Capital Suites #59", "Современный отель у набережной", "Москва", "Russia", None, 4403),
            Hotel(60, "Capital Suites #60", "Историческое здание и высокий сервис", "Санкт-Петербург", "Russia", 2,
                  4201),
            Hotel(61, "Luxury Lounge #61", "Апартаменты с кухней", "Санкт-Петербург", "Russia", 3, 3633),
            Hotel(62, "Novotel City #62", "Апартаменты с кухней", "Санкт-Петербург", "Russia", 2, 3119),
            Hotel(63, "River View Hotel #63", "Рядом с метро и музеями", "Санкт-Петербург", "Russia", 2, 1195),
            Hotel(64, "Eastern Light #64", "Историческое здание и высокий сервис", "Санкт-Петербург", "Russia", 5, 2556),
            Hotel(65, "Fontanka Light #65", "Просторные номера и ресторан", "Санкт-Петербург", "Russia", 2, 1574),
            Hotel(66, "City Comfort #66", "Апартаменты с кухней", "Санкт-Петербург", "Russia", 2, 2821),
            Hotel(67, "Hermitage Suites #67", "Просторные номера и ресторан", "Санкт-Петербург", "Russia", 2, 4822),
            Hotel(68, "Aurora Palace #68", "Бюджетный отель с качественным сервисом", "Москва", "Russia", 3, 3439),
            Hotel(69, "Nevsky Boutique #69", "Тихое место с панорамным видом", "Москва", "Russia", None, 2103),
            Hotel(70, "Fontanka Inn #70", "Историческое здание и высокий сервис", "Москва", "Russia", 4, 2937),
            Hotel(71, "Metro City #71", "Историческое здание и высокий сервис", "Санкт-Петербург", "Russia", None, 2743),
            Hotel(72, "Тверская Премьер #72", "Просторные номера и ресторан", "Москва", "Russia", 4, 3274),
            Hotel(73, "SkyLine Plaza #73", "Рядом с метро и музеями", "Санкт-Петербург", "Russia", 2, 1779),
            Hotel(74, "Мост Отель #74", "Уютный номер и вид на парк", "Санкт-Петербург", "Russia", 5, 1644),
            Hotel(75, "Парк Премьер #75", "Уютный номер и вид на парк", "Санкт-Петербург", "Russia", 4, 4646),
            Hotel(76, "Гранд Отель Москва #76", "Современный отель у набережной", "Москва", "Russia", None, 2435),
            Hotel(77, "Hermitage Suites #77", "Апартаменты с кухней", "Санкт-Петербург", "Russia", 5, 4279),
            Hotel(78, "Heritage Place #78", "Уютный номер и вид на парк", "Москва", "Russia", 4, 4384),
            Hotel(79, "Art Hotel #79", "Просторные номера и ресторан", "Санкт-Петербург", "Russia", None, 1030),
            Hotel(80, "Eastern Light #80", "Историческое здание и высокий сервис", "Москва", "Russia", None, 1238),
            Hotel(81, "Old Town Stay #81", "Апартаменты с кухней", "Москва", "Russia", 3, 2905),
            Hotel(82, "SkyLine Plaza #82", "Бюджетный отель с качественным сервисом", "Москва", "Russia", 2, 1530),
            Hotel(83, "Галерея Отель #83", "Апартаменты с кухней", "Москва", "Russia", 5, 3999),
            Hotel(84, "Vintage Inn #84", "Тихое место с панорамным видом", "Санкт-Петербург", "Russia", 4, 3994),
            Hotel(85, "Palace Line #85", "Историческое здание и высокий сервис", "Москва", "Russia", None, 4981),
            Hotel(86, "Мост Отель #86", "Комфорт и роскошь в центре города", "Санкт-Петербург", "Russia", 5, 1758),
            Hotel(87, "Sokolniki Inn #87", "Тихое место с панорамным видом", "Санкт-Петербург", "Russia", 2, 2563),
            Hotel(88, "Парк Премьер #88", "Современный отель у набережной", "Санкт-Петербург", "Russia", 2, 2735),
            Hotel(89, "Fontanka Light #89", "Историческое здание и высокий сервис", "Москва", "Russia", 3, 4333),
            Hotel(90, "Sky Palace #90", "Рядом с метро и музеями", "Санкт-Петербург", "Russia", 5, 1895),
            Hotel(91, "Aurora Palace #91", "Бюджетный отель с качественным сервисом", "Москва", "Russia", 3, 2104),
            Hotel(92, "Сити Хаус #92", "Уютный номер и вид на парк", "Москва", "Russia", 4, 3649),
            Hotel(93, "Eastern Light #93", "Комфорт и роскошь в центре города", "Санкт-Петербург", "Russia", 5, 1483),
            Hotel(94, "Парк Премьер #94", "Апартаменты с кухней", "Санкт-Петербург", "Russia", None, 2829),
            Hotel(95, "Sunny Place #95", "Рядом с метро и музеями", "Санкт-Петербург", "Russia", None, 2950),
            Hotel(96, "Hermitage Suites #96", "Уютный номер и вид на парк", "Москва", "Russia", 2, 4037),
            Hotel(97, "Palace Line #97", "Просторные номера и ресторан", "Санкт-Петербург", "Russia", 4, 1657),
            Hotel(98, "Metro City #98", "Рядом с метро и музеями", "Санкт-Петербург", "Russia", 5, 3737),
            Hotel(99, "Imperial Garden #99", "Историческое здание и высокий сервис", "Москва", "Russia", 2, 2844),
            Hotel(100, "Пушкин Вест #100", "Комфорт и роскошь в центре города", "Санкт-Петербург", "Russia", None, 4045)
        ]

        return [hotel for hotel in hotels if hotel.city == self.city]


@app.get("/search")
async def search(city: Optional[str] = None, check_in: Optional[str] = None, check_out: Optional[str] = None):
    try:
        service = HotelSearchService(city, check_in, check_out)
        hotels = service.search()
        return JSONResponse(
            content={
                "status": "ok",
                "code": 0,
                "data": {
                    "hotels": [hotel.to_dict() for hotel in hotels]
                }
            }
        )
    except CityValidationException as e:
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "code": e.code,
                "message": e.message
            }
        )
    except DateSearchValidationException as e:
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "code": e.code,
                "message": e.message
            }
        )
