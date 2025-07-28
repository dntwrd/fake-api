from exceptions.hotels.hotel_search_exception import CityValidationException
from models import Hotel
from typing import Optional, List
from datetime import date
from validators import MethodValidator, DateSearchValidator, CityValidator
from data import hotels

class HotelSearchService:
    def __init__(self, city: str, check_in: Optional[date], check_out: Optional[date], current_method: str, correct_method: str):
        self.city = city
        self.check_in = check_in
        self.check_out = check_out
        self.current_method = current_method
        self.correct_method = correct_method

    def search(self):
        CityValidator.validate(self.city)
        DateSearchValidator.validate(self.check_in, self.check_out)
        MethodValidator.validate(self.current_method, self.correct_method)

        return [hotel for hotel in hotels if hotel.city == self.city]