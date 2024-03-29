import json
from typing import List
import httpx


class AutomaticSearchController:
    def __init__(self):
        self.capacity = 0
        self.rate__gte = 0
        self.area__lte = 0
        self.area__gte = 0
        self.reserve_date_before = ""
        self.reserve_date_after = ""

    def set_capacity(self, capacity):
        self.capacity = capacity

    def set_min_rate(self, min_rate):
        self.rate__gte = min_rate

    def set_min_area_size(self, min_area_size):
        self.area__gte = min_area_size

    def set_max_area_size(self, max_area_size):
        self.area__lte = max_area_size

    def set_min_reserve_date(self, min_reserve_date):
        self.reserve_date_after = min_reserve_date

    def set_max_reserve_date(self, max_reserve_date):
        self.reserve_date_before = max_reserve_date

    base_url = "http://127.0.0.1:8080/"
    get_places_offset = "api/place/get/"

    def get_params(self):
        return self.__dict__

    @classmethod
    def parse_json_bytes(cls, b):
        parsed = b.decode("utf-8")
        return json.loads(parsed)

    def get_places(self) -> List:
        with httpx.Client() as client:
            response = client.get(
                url=self.base_url + self.get_places_offset, params=self.get_params()
            )
        return self.parse_json_bytes(response.content)
