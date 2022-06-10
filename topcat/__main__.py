import argparse
from datetime import datetime, timedelta

from .poll import poll_venue


def _parse_args() -> argparse.Namespace:
    args = argparse.ArgumentParser(
        description="""
Poll a venue on ontopo for table availability,
and send an email with updates every `interval` minutes.
""",
    )

    args.add_argument("email", help="Email to send table updates to")
    args.add_argument("venue_id", help="Venue to poll (example: 'ocd')")
    args.add_argument(
        "-d",
        "--start-date",
        help="Start date to poll (default - one week from today)",
        default=(datetime.today() + timedelta(weeks=1)),
        type=lambda s: datetime.strptime(s, "%Y-%m-%d"),
    )
    args.add_argument(
        "-i",
        "--interval",
        default=10,
        help="Interval for checking availability (in minutes)",
        type=int,
    )
    args.add_argument(
        "-s",
        "--table-size",
        default=4,
        help="Size of table (# of people)",
    )

    return args.parse_args()


def _format_date(date: datetime) -> str:
    return date.strftime("%Y-%m-%d")


def main():
    args = _parse_args()
    print(f"[+] Checking availability at '{args.venue_id}'")
    print(
        f"[+] From: {_format_date(args.start_date)} until "
        f"{_format_date(args.start_date + timedelta(weeks=1))} (at 20:00), "
        f"a table for {args.table_size}",
    )
    print(f"[+] Email to send updates to: {args.email}")

    poll_venue(
        email=args.email,
        start_date=args.start_date,
        interval=args.interval,
        table_size=args.table_size,
        venue_id=args.venue_id,
    )


if __name__ == "__main__":
    main()
