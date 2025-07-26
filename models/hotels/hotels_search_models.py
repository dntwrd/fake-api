from typing import Optional

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