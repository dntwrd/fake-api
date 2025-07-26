from .hotels.hotel_search import app as hotel_search
from .hotels.rooms_search import app as rooms_search

hotels_routers = [
    hotel_search, rooms_search
]
