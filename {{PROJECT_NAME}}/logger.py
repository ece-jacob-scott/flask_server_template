import logging

from flask import Flask, has_request_context, request
from http.client import HTTPConnection


# %a  Locale’s abbreviated weekday name.
# %A  Locale’s full weekday name.
# %b  Locale’s abbreviated month name.
# %B  Locale’s full month name.
# %c  Locale’s appropriate date and time representation.
# %d  Day of the month as a decimal number [01,31].
# %H  Hour (24-hour clock) as a decimal number [00,23].
# %I  Hour (12-hour clock) as a decimal number [01,12].
# %j  Day of the year as a decimal number [001,366].
# %m  Month as a decimal number [01,12].
# %M  Minute as a decimal number [00,59].
# %p  Locale’s equivalent of either AM or PM. (1)
# %S  Second as a decimal number [00,61]. (2)
# %U  Week number of the year (Sunday as the first day of the week) as a decimal number [00,53]. All days in a new year preceding the first Sunday are considered to be in week 0.    (3)
# %w  Weekday as a decimal number [0(Sunday),6].
# %W  Week number of the year (Monday as the first day of the week) as a decimal number [00,53]. All days in a new year preceding the first Monday are considered to be in week 0.    (3)
# %x  Locale’s appropriate date representation.
# %X  Locale’s appropriate time representation.
# %y  Year without century as a decimal number [00,99].
# %Y  Year with century as a decimal number.
# %z  Time zone offset indicating a positive or negative time difference from UTC/GMT of the form +HHMM or -HHMM, where H represents decimal hour digits and M represents decimal minute digits [-23:59, +23:59].
# %Z  Time zone name (no characters if no time zone exists).
# %%  A literal '%' character.


class RequestFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.remote_addr = request.remote_addr
            record.request_id = request.id
        else:
            record.url = None
            record.remote_addr = None
            record.request_id = None
        return super().format(record)


# Flask uses the root logger, so we need to configure that
def setup_logging():
    root_logger = logging.getLogger()

    request_log_formatter = RequestFormatter(
        fmt="[%(asctime)s] %(request_id)s - %(url)s - %(remote_addr)s - %(levelname)s - %(name)s: %(message)s",
        datefmt="%Y/%m/%d %H:%M:%S %z%Z",
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(request_log_formatter)

    root_logger.addHandler(console_handler)

    # setup logging for HTTPConnection (used by requests)
    HTTPConnection.debuglevel = 1
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True
    for handler in requests_log.handlers:
        requests_log.removeHandler(handler)
    requests_log.addHandler(console_handler)