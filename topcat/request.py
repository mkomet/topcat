import datetime
import enum
from typing import List, Optional

import requests
from pydantic import BaseModel, Extra

from topcat.const import EN_US_LOCALE, SEARCH_VENUE_SLUG, ONTOPO_AVAILABILITY_API, ONTOPO_SEARCH_VENUE_API, \
    ONTOPO_FETCH_VENUE_API

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


class VenueSearch(BaseModel):
    slug: str
    version: int
    title: str
    address: str


class Venue(BaseModel):
    title: str
    slug: str
    version: int


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


def search_venue(venue: str) -> Venue:
    venue_search = VenueSearch(**requests.get(ONTOPO_SEARCH_VENUE_API, params=dict(
        slug=SEARCH_VENUE_SLUG,
        locale=EN_US_LOCALE,
        terms=venue
    )).json()[0])

    return Venue(**requests.get(ONTOPO_FETCH_VENUE_API, params=dict(
        slug=venue_search.slug,
        locale=EN_US_LOCALE,
        version=venue_search.version
    )).json()["pages"][0])


def search_availability(table_size: int, date: datetime.datetime, venue: str) -> VenueAvailability:
    # Build POST body
    criteria = dict(
        date=date.strftime("%Y%m%d"),
        time=date.strftime("%H%M"),
        size=str(table_size),
    )

    payload = dict(
        criteria=criteria,
        locale=EN_US_LOCALE,
        slug=search_venue(venue).slug,
    )

    response = requests.post(
        url=ONTOPO_AVAILABILITY_API,
        json=payload,
    )
    # print(response.json())
    return VenueAvailability(**response.json())
