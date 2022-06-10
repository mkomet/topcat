import datetime
import fire

from topcat import VenueAvailability, search_availability
from topcat.request import BookingMethod

def cli(restaurant: str, start_date_str: str, end_date_str: str):
    start_date = datetime.datetime.strptime(start_date_str, '%d/%m/%y-%H:%M')
    end_date = datetime.datetime.strptime(end_date_str, '%d/%m/%y-%H:%M')
    date_generated = [start_date + datetime.timedelta(days=x) for x in range(0, (end_date-start_date).days)]

    for date in date_generated:
        availability = search_availability(2, date, restaurant)
        for area in availability.areas or []:
            for option in area.options or []:
                if (option.method == BookingMethod.SEAT):
                    print(f"date: {date} time: {option.time}")


if __name__ == "__main__":
    fire.Fire(cli)
