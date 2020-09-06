from datetime import datetime
from varname import varname, nameof
from time import sleep
from collections import Counter
from pendulum.datetime import DateTime
import pendulum


class TradingViewDateTime(DateTime):
    def to_timestamp_function(self):
        return (
            f"timestamp({self.year}, "
            f"{self.month}, "
            f"{self.day}, "
            f"{self.hour}, "
            f"{self.minute}, "
            f"{self.second})"
        )

    @classmethod
    def parse(cls, dt):
        parsed = pendulum.parse(dt)
        return cls(year=parsed.year, month=parsed.month, day=parsed.day)

    def __str__(self):
        return self.to_timestamp_function()

    def __repr__(self):
        return self.to_timestamp_function()


# tvdt = TradingViewDateTime.now()
# print(tvdt.int_timestamp)

x = TradingViewDateTime.parse("2015-02-02")
print(x)

exit()
import random

SHOW = False

print(f"var {nameof(SHOW)} = {str(SHOW).lower()}")
print(f"{nameof(SHOW)} = {str(SHOW).lower()}")
c = Counter()
for _ in range(5):
    # print([expiration, 61.50, 75.0])
    # c[expiration] += 1
    while random.random() > 0.5:
        expiration = TradingViewDateTime.now()
        c[expiration.int_timestamp] += 1
        # print(c.most_common())
    sleep(1)
print(c)
print(c.most_common())
