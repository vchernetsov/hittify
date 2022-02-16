import random


CONSUMPTION_WINDOW = 5  # 5 minutes
WINDOWS = 2 * 6 * 24 * 7 * 4  # 1 month


class ConsumeEvent:
    water_debt = None
    debt_from = debt_to = None
    min_consumption =  max_consumption = None

    def __init__(self):
        self.water_debt = random.randint(self.debt_from, self.debt_to)
        self.starts_at = ...

    def consume(self):
        self.water_debt -= random.randint(15, 30)



class MorningWash(ConsumeEvent):
    debt_from = 80
    debt_from = 100
    min_consumption = 15
    max_consumption = 35

class WaterConsumer:

    def cancel(self):
        """Process cancel events"""
        pass

    def fix_added(self):
        """
            Fix regular event which must be done at an condition
            but obviously can not be done, when person is absent.
            So just whif it to the next active day
        """
        pass

    def iterate(self):
        self.add()
        self.cancel()
        self.fix_added()

    def add(self):
        """Process adding events"""
        for week in range(1, 5):
            print (f"week={week}")
            self.over_week()

    def over_week(self):
        """Iterate water consumption over week"""
        for weekday in range(1, 8):
            print (f"\tweekday={weekday}")
            self.over_day()

    def over_day(self):
        """Iterate water consumption over day"""
        way_windows = 2 * 6 * 24
        for window in range(1, way_windows):
            print (f"\t\twindow={window}")


water_consumer = WaterConsumer()
water_consumer.iterate()
