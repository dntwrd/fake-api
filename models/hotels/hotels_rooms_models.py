from datetime import date
from typing import Optional

class Room:
    def __init__(self, hotel_id: int, hotel_name: str, room_id: int, room_name: str, room_description: str, price: int):
        self.hotel_id = hotel_id
        self.hotel_name = hotel_name
        self.room_id = room_id
        self.room_name = room_name
        self.room_description = room_description
        self.price = price

    def to_dict(self):
        return {
            'hotel_id': self.hotel_id,
            'hotel_name': self.hotel_name,
            'room_id': self.room_id,
            'room_name': self.room_name,
            'room_description': self.room_description,
            "price": self.price
        }