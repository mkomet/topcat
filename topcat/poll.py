import datetime
import time
from typing import Dict

from .request import BookingMethod, VenueAvailability, search_availability

_MAIL_FORMAT = """
<!DOCTYPE html>
<html>
<body>
{body}
</body>
</html>
"""
_NEW_AVAILABILITY_FORMAT = """Date: {date}
{availability}
"""


def _send_mail(
    email: str,
    new_availabilities: Dict[datetime.datetime, VenueAvailability],
) -> None:
    availabilities_str = "\n".join(
        _NEW_AVAILABILITY_FORMAT.format(
            date=date.strftime("%d/%m/%Y"),
            availability=availability.to_html(),
        )
        for date, availability in new_availabilities.items()
    )
    body = _MAIL_FORMAT.format(body=availabilities_str)
    print(body)


def poll_venue(
    email: str,
    start_date: datetime.datetime,
    table_size: int,
    interval: int,
    venue_id: str,
):
    found_availabilities: Dict[int, VenueAvailability] = dict()
    while True:
        new_availabilities: Dict[
            datetime.datetime,
            VenueAvailability,
        ] = dict()
        for day_delta in range(7):
            date = start_date + datetime.timedelta(days=day_delta)
            availability = search_availability(
                table_size=table_size,
                date=date,
                venue=venue_id,
            )

            if availability.method == BookingMethod.DISABLED:
                print(
                    "[-] No booking options for ",
                    f"{date.strftime('%d/%m/%Y')}",
                )
                continue

            current_found_availability = found_availabilities.get(day_delta)
            if (
                current_found_availability is None
                or current_found_availability != availability
            ):
                found_availabilities[day_delta] = availability
                new_availabilities[date] = availability
            else:
                print(
                    "[-] Skipping known booking options for "
                    f"{date.strftime('%d/%m/%Y')}",
                )

        if len(new_availabilities) > 0:
            _send_mail(email, new_availabilities)

        time.sleep(interval * 60)
