import random


CONSUMPTION_WINDOW = 5  # 5 minutes
HOUR = 2 * 6
WINDOWS = 2 * 6 * 24 * 7 * 4  # 1 month

class Event:
    water_debt = debt_from = debt_to = None
    min_consumption =  max_consumption = None
    starts_at = starts_from = starts_to = None
    possibility = None
    name = None

    @property
    def happens(self):
        return random.randrange(0, 101) < self.possibility

    def __init__(self, week, weekday):
        self.week = week
        self.weekday = weekday

    def __repr__(self):
        return (
            f"""{self.name}\t"""
            f"""\tweek: {self.week},"""
            f"""\tweekday: {self.weekday},"""
            f"""\tstarts_at: {self.starts_at},"""
            f"""\tdebt:{self.water_debt}"""
        )


class ConsumeEvent(Event):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.water_debt = random.randrange(self.debt_from, self.debt_to)
        self.starts_at = random.randrange(self.starts_from, self.starts_to)

    def consume(self):
        consumption = random.randrange(self.min_consumption, self.max_consumption)

        if consumption >= self.water_debt:
            consumption = self.water_debt
        self.water_debt -= consumption
        print (f"{self.name} consumed {consumption}")
        return consumption


class MorningWash(ConsumeEvent):
    name = 'Morning wash'
    debt_from = 80
    debt_to = 120
    min_consumption = 15
    max_consumption = 35
    starts_from = HOUR * 8 - 2
    starts_to = HOUR * 8 + 2
    possibility = 80


class BathWash(ConsumeEvent):
    name = 'Bath wash'
    debt_from = 280
    debt_to = 320
    min_consumption = 100
    max_consumption = 120
    starts_from = HOUR * 22 - 2
    starts_to = HOUR * 22 + 2
    possibility = 60


class DishWash(ConsumeEvent):
    name = 'Dish wash'
    debt_from = 29
    debt_to = 30
    min_consumption = 10
    max_consumption = 10
    starts_from = HOUR * 20
    starts_to = HOUR * 21
    possibility = 100

    def __init__(self, week, weekday):
        super().__init__(week, weekday)
        self.water_debt = 30
        self.ticks = 6
    
    def consume(self):
        """Consume water every second time window"""
        consumption = 10
        if not self.ticks % 2:
            self.water_debt -= consumption
        else:
            consumption = 0
        self.ticks -= 1
        print (f"{self.name} consumed {consumption}")
        return consumption

class WashMashine(ConsumeEvent):
    name = "Washing mashine"
    debt_from = 29
    debt_to = 30
    min_consumption = 10
    max_consumption = 10
    starts_from = HOUR * 20
    starts_to = HOUR * 21
    possibility = 100

    def __init__(self, week, weekday):
        super().__init__(week, weekday)
        self.ticks = 12
    
    def consume(self):
        """Consume water every fourth time window"""
        consumption = 10
        if not self.ticks % 4:
            self.water_debt -= consumption
        else:
            consumption = 0
        self.ticks -= 1
        print (f"{self.name} consumed {consumption}")
        return consumption


class CancelEvent(Event):
    pass


class Sauna(CancelEvent):
    name = "Sauna"
    possibility = 50

    @property
    def happens(self):
        if self.weekday == 5 and random.randrange(0, 101) < self.possibility:
            return True
        return False



class Trip(CancelEvent):
    name = "Trip"
    possibility = 75


    @property
    def happens(self):
        days = self.week * 7 + self.weekday
        if ((not days % 10) or (not days % 11)) and (random.randrange(0, 101) < self.possibility):
            return True
        return False

class WaterConsumer:

    def generate(self):
        """Declare events"""
        days = 0
        for week in range(1, 5):
            print (f"week: {week}")
            for weekday in range(1, 8):
                print (f"weekday: {weekday}")
                events = []
                sauna = Sauna(week=week, weekday=weekday)
                if sauna.happens:
                    continue
                trip = Trip(week=week, weekday=weekday)
                if trip.happens:
                    continue
                morning_wash = MorningWash(week=week, weekday=weekday)
                if morning_wash.happens:
                    events.append(morning_wash)
                bath_wash = BathWash(week=week, weekday=weekday)
                if bath_wash.happens:
                    events.append(bath_wash)
                dish_wash = DishWash(week=week, weekday=weekday)
                if dish_wash.happens:
                    events.append(dish_wash)
                if weekday == 6:
                    washing_mashine = WashMashine(week=week, weekday=weekday)
                    if washing_mashine.happens:
                        events.append(washing_mashine)
                for consumption in self.weekly_consume(events):
                    yield consumption

    def weekly_consume(self, events):
        windows = HOUR * 24
        for window in range(1, windows):
            window_consumption = 0
            for event in events:
                if window >= event.starts_at and event.water_debt:
                    window_consumption += event.consume()
            yield window_consumption


water_consumer = WaterConsumer()
fh = open('monthly.txt', 'w')
for x in water_consumer.generate():
    fh.write(f"{x}\n")
fh.close()
