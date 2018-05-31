import os
import datetime
import shelve
from config import DB_NAME
import db

if __name__ == '__main__':
    if os.path.exists(DB_NAME + '.dat'): os.unlink(DB_NAME + '.dat')
    if os.path.exists(DB_NAME + '.bak'): os.unlink(DB_NAME + '.bak')
    if os.path.exists(DB_NAME + '.dir'): os.unlink(DB_NAME + '.dir')

    now = datetime.datetime.now()
    data = shelve.open(DB_NAME)
    db.add_date(data, db.make_date(now.day, now.month, now.year))
    db.add_film(data, db.make_date(now.day, now.month, now.year),
                'Мстители: Война Бесконечности', [['13:00', 0], ['14:00', 1], ['19:00', 0], ['23:00', 0]])
    db.add_film(data, db.make_date(now.day, now.month, now.year),
                'Дэдпул 2', [['09:15', 2],['11:20', 2],['15:40', 2],['18:07', 2],['20:00', 2]])
    db.add_film(data, db.make_date(now.day, now.month, now.year),
                'Третье убийство', [['13:00', 1],['16:30', 1],['19:45', 1],['21:40', 1],['23:01', 1]])
    db.add_film(data, db.make_date(now.day, now.month, now.year),
                'Истерия', [['10:00', 2],['12:15', 2],['17:25', 2],['20:40', 2]])
    db.add_film(data, db.make_date(now.day, now.month, now.year),
                'Тренер', [['10:30',0],['14:35',0],['17:50',0],['22:00',0],])
    db.add_film(data, db.make_date(now.day, now.month, now.year),
                'Редкая бабочка', [['15:00', 1],['20:10', 1]])
    db.add_date(data, db.make_date(now.day + 1, now.month, now.year))
    db.add_film(data, db.make_date(now.day, now.month, now.year),
                'Тренер', [['10:30',0],['14:35',0],['17:50',0],['22:00',0],])
    db.add_film(data, db.make_date(now.day, now.month, now.year),
                'Дэдпул 2', [['09:15', 2],['11:20', 2],['15:40', 2],['18:07', 2],['20:00', 2]])
    db.add_film(data, db.make_date(now.day, now.month, now.year),
                'Тренер', [['10:30',0],['14:35',0],['17:50',0],['22:00',0],])
    db.add_film(data, db.make_date(now.day + 1, now.month, now.year),
                'Такси 5', [['08:50', 0], ['11:05', 1], ['16:00', 1], ['21:20', 1]])
    db.add_film(data, db.make_date(now.day + 1, now.month, now.year),
                'Красавица для чудовища', [['10:00', 0], ['13:45', 0], ['19:15', 0]])
    db.add_film(data, db.make_date(now.day, now.month, now.year),
                'Редкая бабочка', [['15:00', 1],['20:10', 1]])
    db.add_film(data, db.make_date(now.day + 1, now.month, now.year),
                'Муза смерти', [['12:00', 0], ['16:30', 1], ['22:30', 0]])
    db.add_date(data, db.make_date(now.day + 2, now.month, now.year))
    db.add_film(data, db.make_date(now.day, now.month, now.year),
                'Тренер', [['10:30',0],['14:35',0],['17:50',0],['22:00',0],])
    db.add_film(data, db.make_date(now.day, now.month, now.year),
                'Дэдпул 2', [['09:15', 2],['11:20', 2],['15:40', 2],['18:07', 2],['20:00', 2]])
    db.add_film(data, db.make_date(now.day + 2, now.month, now.year),
                'Чудеса', [['10:00', 0],['13:10', 0],['18:20', 0],['21:30', 0]])
    db.add_film(data, db.make_date(now.day + 2, now.month, now.year),
                'За бортом', [['12:00', 0], ['14:00', 0], ['17:00', 0], ['22:00', 0]])
    db.add_film(data, db.make_date(now.day, now.month, now.year),
                'Тренер', [['10:30',0],['14:35',0],['17:50',0],['22:00',0],])
    db.add_film(data, db.make_date(now.day, now.month, now.year),
                'Редкая бабочка', [['15:00', 1],['20:10', 1]])
    #print(list(data.items()))
    data.close()
