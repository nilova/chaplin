import re

class knowledge_base:
    class film_time_type:
        def __init__(self):
            self.time = None
            self.hours = None
            self.minutes = None
            self.pmam = None
            self.half = None
    def __init__(self, is_first=True):
        self.is_first = is_first
        self.is_schedule = True
        self.film_name = None
        self.is_film_price = False
        self.film_time = knowledge_base.film_time_type()
        self.is_ticket_for = False

    @staticmethod
    def split_words(msg):
        return list(filter(None, str.split(re.sub(
            r'[^\w\s]|_', r' ', msg).lower())))