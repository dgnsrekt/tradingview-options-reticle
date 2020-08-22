from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional
from datetime import date
from pprint import pprint
import yfinance as yf
import pendulum

TODAY = pendulum.now().start_of("day")
PROCESS_DATE = TODAY.subtract(days=1)
FUTURE_DATE = TODAY.add(days=10)

PERIOD = FUTURE_DATE - PROCESS_DATE
FUTURE_OFFSET = PERIOD.in_days()

# print(PROCESS_DATE)
# print(FUTURE_DATE)
# print(PERIOD.in_days())

CODE_BLOCK = f"PROCESS_DATE = year == {PROCESS_DATE.year} and month == {PROCESS_DATE.month} and dayofmonth == {PROCESS_DATE.day}"
print(CODE_BLOCK)

CODE_BLOCK = "plotchar(PROCESS_DATE)"
print(CODE_BLOCK)

CODE_BLOCK = f"plotchar(PROCESS_DATE, offset={FUTURE_OFFSET})"
print(CODE_BLOCK)
