import datetime

from topcat import search_availability
from topcat.request import BookingMethod


def test_availability():
    next_week = datetime.datetime(2022, 6, 13, 20, 0, 0)

    availability = search_availability(2, next_week, "texasbbqtlv")
    assert availability.method == BookingMethod.SEAT


def test_no_availability():
    availability = search_availability(6, datetime.datetime.now(), "ocd")
    assert availability.method == BookingMethod.DISABLED
