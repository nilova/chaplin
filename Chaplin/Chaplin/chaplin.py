import datetime, db, kb, chaplin_gui

class chatbot:
    monthes_names = ['января', 'февраля', 'марта', 'апреля', 
                     'мая', 'июня', 'июля', 'августа', 
                     'сентября', 'октября', 'ноября', 'декабря']

    def __init__(self, data, base, morph):
        self.data = data
        self.base = base
        self.morph = morph
        now = datetime.datetime.now()
        self.date = db.make_date(now.day, now.month, now.year)
        self.now = db.make_date(now.day, now.month, now.year)

    def _get_norm(self, word):
        return self.morph.normal_forms(word)[0]

    def check_change_schedule(self, msg):
        for check in ['показать', 'показывать',
            'расписание', 'прокат', 'идти']:
            if check in msg:
                for i, t in enumerate(['сегодня',
                    'завтра', 'послезавтра']):
                    if t in msg:
                        #day, month, year = self.now.split('.')
                        #d = datetime.datetime(int(year), int(month), int(day), 0, 0, 0)
                        d = datetime.datetime.now() + datetime.timedelta(days=i)
                        self.date = db.make_date(d.day, d.month, d.year)
                        self.print_schedule()
                        return

    def split_four_numbers(self, msg):
        i = 0
        while i < len(msg):
            if len(msg[i]) == 4:
                try:
                    int(msg[i])
                    num1, num2 = msg[i][:2], msg[i][2:]
                    msg[i] = num1
                    msg.insert(i + 1, num2)
                except ValueError: pass
            i += 1

    #def cut_ticket_for(self, msg):
    #    for i in range(1, len(msg)):
    #        if msg[i] == 'билет':
    #            del msg[i - 1]

    def check_film_name(self, msg):
        for film in db.get_films_names(self.data, self.date):
            count = 0
            msg_overI = []
            film_words = kb.knowledge_base.split_words(film)
            for film_word in film_words:
                film_word_norm = self._get_norm(film_word)
                if film_word_norm in msg:
                    count += 1
                    msg_overI.append(msg.index(film_word_norm))
            if count >= 2 or (len(film_words) == 1 and count == 1):
                self.base.film_name = film
                for i in range(len(msg_overI)):
                    del msg[msg_overI[i] - i]
                break

    def _check_number(self, st, nxt):
        nums = ['HOOK', 'один', 'два', 'три', 'четыре',
         'пять', 'шесть', 'семь', 'восемь', 'девять',
         'десять', 'одиннадцать', 'двенадцать',
         'тринадцать', 'четырнадцать', 'пятнадцать',
         'шестнадцать', 'семнадцать', 'восемнадцать',
         'девятнадцать']
        tens = ['ноль', 'HOOK', 'двадцать',
                'тридцать', 'сорок', 'пятьдесят']
        st = self._get_norm(st)
        nxt = self._get_norm(nxt)
        try: num = int(st); return num, 1
        except ValueError: pass
        try:
            index = nums.index(st);
            if nxt != 'час': return index, 1
            else: return index, 2
        except ValueError:
            if st == 'первое': return 1, 1
            if st == 'третье': return 3, 1
        if st == 'час': return 1, 1
        try:
            index = tens.index(st)
            try:
                index2 = nums[1:10].index(nxt)
                return index * 10 + index2 + 1, 2
            except ValueError:
                if nxt == 'первое': return index * 10 + 1, 2
                if nxt == 'третье': return index * 10 + 3, 2
                if nxt == 'ноль': return index * 10, 2
                else: return index * 10, 1
        except ValueError: pass
        return None, 0

    def check_film_time(self, msg):
        pmam = ['день', 'вечер', 'полдень', 'полночь', 'полуночь']
        half = ['половина', 'четверть']
        ft = self.base.film_time
        ft.pmam = None
        for w in msg:
            if w in pmam: ft.pmam = w
            if w in half: ft.half = w           
        if not ft.pmam in pmam[-3:]:
            for i in range(len(msg)):
                next_word = msg[i+1] if i != len(msg)-1 else ''
                num_h, num_h_count = self._check_number(msg[i], next_word)
                if num_h != None:
                    if ft.minutes == None:
                        if i < len(msg) - num_h_count:
                            next_word = msg[i+num_h_count+1] if i != len(msg)-num_h_count-1 else ''
                            num_m, num_m_count = self._check_number(msg[i+num_h_count], next_word)
                            if num_m != None:
                               ft.hours = num_h
                               ft.minutes = num_m
                               break
                            elif self._get_norm(msg[i+num_h_count]) == 'минута':
                               ft.minutes = num_h
                            elif ft.hours == None: ft.hours = num_h
                        elif ft.hours == None: ft.hours = num_h; break
                    else:
                        if i < len(msg) - num_h_count and \
                            self._get_norm(msg[i+num_h_count]) == 'часы':
                            ft.hours = num_h; break
                        else: ft.hours = num_h - 1; break
        else: ft.hours = 0 if ft.pmam in pmam[-2:] else 12; ft.minutes = 0
        if not ft.hours in range(0, 25): ft.hours = None
        if ft.pmam in pmam[0:2] and not ft.hours in range(0, 13): ft.hours = None
        elif not ft.minutes in range(0, 60): ft.minutes = None
        if ft.hours != None:
            if ft.pmam in pmam[0:2]: ft.hours += 12
            ft.hours %= 24
            if ft.minutes == None: ft.minutes = 0
            if ft.half != None:
                d = datetime.datetime(1970, 1, 1, ft.hours, ft.minutes, 0)
                span = 30 if ft.half == half[0] else 45
                d -= datetime.timedelta(minutes=span)
                ft.hours = d.hour
                ft.minutes = d.minute
            ft.time = '%02d:%02d' % (ft.hours, ft.minutes)
            ft.hours = ft.minutes = ft.half = None
        else: self.base.film_time = kb.knowledge_base.film_time_type()

    def check_film_price(self, msg):
        for check in ['почем', 'сколько стоит',
            'сколько стоят', 'какую цену']:
            count = 0
            check_words = kb.knowledge_base.split_words(check)
            for check_word in check_words:
                check_word_norm = self._get_norm(check_word)
                if check_word_norm in msg: count += 1
            if count == len(check_words):
                self.base.is_film_price = True; break

    def print_schedule(self):
        if self.base.is_first:
            self.base.is_first = False
            print('Добро пожаловать в CHAPLIN! ', end='')
        print('Расписание на ' + 
            self.date[:self.date.index('.')] + ' ' +\
            chatbot.monthes_names[datetime.datetime.now().month - 1] + ', у нас в прокате:\n')
        for film in db.get_films_names(self.data, self.date):
            line = '  ' + film + ' ' * (30 - len(film))
            for time in db.get_times_by_film(self.data, self.date, film):
                line += time + ' '
            print(line)
        print('\nЧаплин: Пожалуйста, выберите сеанс')
        self.base.is_schedule = False

    def chat(self, msg):
        self.check_change_schedule(msg)
        self.check_film_name(msg)
        self.split_four_numbers(msg)
        self.check_film_time(msg)
        self.check_film_price(msg)
        #print('TIME=' + str(self.base.film_time.time))

        if self.base.is_schedule: self.print_schedule()
        elif self.base.is_film_price:
            if self.base.film_name != None:
                print('Чаплин: Цены билетов на фильм ' + self.base.film_name + ':\n')
                for time in db.get_times_by_film(self.data, self.date, self.base.film_name):
                    print('\t' + time + '\t', end='')
                    mn, mx = db.get_minmax_price_by_film_and_time(self.data, self.date, self.base.film_name, time)
                    print(mn, '-', mx, ' руб.', sep='')
            else: print('Чаплин: Цена какого фильма Вас интересует?')
        elif self.base.film_name != None:
            if self.base.film_time.time == None:
                times = db.get_times_by_film(self.data, self.date, self.base.film_name)
                if len(times) == 1: self.base.film_time.time = times[0]
            if self.base.film_time.time != None:
                seats = db.get_seats_by_film_and_time(self.data, self.date, self.base.film_name, self.base.film_time.time)
                if seats != None:
                    def callback_gui(is_success, selected_seats = [], is_book = False):
                        if is_success:
                            db.order_seats(self.data, self.date, self.base.film_name,
                                self.base.film_time.time, selected_seats, is_book)
                            self.base = kb.knowledge_base(False)
                            self.base.is_schedule = False
                            print('Чаплин: Приятного просмотра!')
                        else:
                            self.base = kb.knowledge_base(False)
                            self.print_schedule()
                    chaplin_gui.create_gui(seats, self.base.film_name, self.base.film_time.time, callback_gui)
                else:
                    print('Чаплин: Для фильма ' + self.base.film_name +
                          ' выбранное время отсутствует')
                    print('        Выберите из следующих сеансов:')
                    print('        ', end='')
                    times = db.get_times_by_film(self.data, self.date, self.base.film_name)
                    for time in times[:-1]: print(time, ', ', sep='', end='')
                    print(times[-1])
                    self.base.film_time = kb.knowledge_base.film_time_type()
            pass
