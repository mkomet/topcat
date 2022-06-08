import datetime

import bs4

from topcat import VenueAvailability, search_availability
from topcat.request import BookingMethod


def _check_availability_mail(availability: VenueAvailability) -> None:
    doc = bs4.BeautifulSoup(availability.to_html(), "html.parser")
    assert doc


def test_availability():
    next_week = datetime.datetime(2022, 6, 13, 20, 0, 0)

    availability = search_availability(2, next_week, "texasbbqtlv")
    assert availability.method == BookingMethod.SEAT
    _check_availability_mail(availability)


def test_no_availability():
    availability = search_availability(6, datetime.datetime.now(), "ocd")
    assert availability.method == BookingMethod.DISABLED
    _check_availability_mail(availability)
