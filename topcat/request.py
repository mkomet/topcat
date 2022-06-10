import datetime
import enum
from typing import List, Optional

import requests
from pydantic import BaseModel, Extra

_ONTOPO_URL = "https://ontopo.co.il"
_ONTOPO_AVAILABILITY_API = f"{_ONTOPO_URL}/api/availability/searchAvailability"

_AVAILABLITY_FORMAT = """
{areas}
"""
_BOOKING_AREA_FORMAT = """
<p class="title"><b>
{area}
</b></p>
{options}
"""
_BOOKING_OPTION_FORMAT = """
<p class="story">
{option}
</p>
"""


class BookingMethod(enum.Enum):
    SEAT = "seat"
    DISABLED = "disabled"
    PHONE = "phone"
    STANDBY = "standby"


class BookingOption(BaseModel):
    time: str
    method: BookingMethod
    text: Optional[str]
    id: Optional[str]
    score: Optional[int]

    def to_html(self) -> str:
        return _BOOKING_OPTION_FORMAT.format(
            option=f"{self.time} method={self.method} score={self.score}",
        )


class VenueArea(BaseModel):
    id: str
    icon: str
    text: str
    options: List[BookingOption]
    score: Optional[int]

    def to_html(self) -> str:
        return _BOOKING_AREA_FORMAT.format(
            area=f"{self.icon} score={self.score}",
            options="\n".join(option.to_html() for option in self.options),
        )


class VenueAvailability(BaseModel, extra=Extra.ignore):
    recommended: List[BookingOption]
    method: BookingMethod
    areas: Optional[List[VenueArea]]

    def to_html(self) -> str:
        if self.areas is None:
            return _AVAILABLITY_FORMAT.format(
                areas="No seating available currently",
            )

        return _AVAILABLITY_FORMAT.format(
            areas="\n".join(area.to_html() for area in self.areas),
        )


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
