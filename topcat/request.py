import datetime
import enum
from typing import List, Optional
import requests
from pydantic import BaseModel, Extra


_ONTOPO_URL = "https://ontopo.co.il"
_ONTOPO_AVAILABILITY_API = f"{_ONTOPO_URL}/api/availability/searchAvailability"


class BookingMethod(enum.Enum):
    SEAT = "seat"
    DISABLED = "disabled"


class BookingOption(BaseModel):
    pass


class VenueArea(BaseModel):
    pass


class VenueAvailability(BaseModel, extra=Extra.ignore):
    recommended: List[BookingOption]
    method: BookingMethod
    areas: Optional[List[VenueArea]]


def search_availability(
    table_size: int,
    date: datetime.datetime,
    venue: str,
) -> VenueAvailability:
    # Build POST body
    criteria = dict(
        date=date.strftime("%Y%m%d"),
        time=date.strftime("%H%M"),
        size=str(table_size),
    )
    payload = dict(
        criteria=criteria,
        locale="en",
        page_id=venue,
    )

    response = requests.post(
        url=_ONTOPO_AVAILABILITY_API,
        json=payload,
    )
    return VenueAvailability(**response.json())

