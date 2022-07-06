import datetime as dt


class Record:
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        # Брать тренарную операцию в круглые скобки не обязательно
        # И возможно с учетом ширины строк лучше было бы использовать
        # Конструкцию if else
        self.date = (
            dt.datetime.now().date() if
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        # Нельзя называть переменные именем класса (с совпадением регистра)
        # В данном случае метод должен отработать нормально
        # Но при попытке создать новый объект класса Record в методе
        # интерпретатор попытается вызвать последний объект
        # полученный от итератора. Потому что под этим именем здесь он
        # запомнил именно объект, а не класс. Можно почитать про LEGB
        for Record in self.records:
            if Record.date == dt.datetime.now().date():
                # += было бы лаконичнее. Необходимости в явном использовании
                # оператора + нет
                today_stats = today_stats + Record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        # В будующем подобные конструкции можно заменить на
        # итераторы из модуля itertools, например summ(filter(...))
        for record in self.records:
            # Скобки в if избыточны
            # Вместо длинного условия if можно и лучше
            # записать оба условия в логические переменные
            # и преобразовать if в if not is_week_expired and if not today
            if (
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        x = self.limit - self.get_today_stats()
        if x > 0:
            # Кодстайл запрещает использование переносов через бэкслеш. (\)
            # Но в данном случае его лучше не использовать в принципе.
            # Строковые возвращаемые объекты лучше явно инициализировать
            # и записывать в переменную. resulting_report = "..."
            # Для многострочных комментариев можно использовать
            # строки """ c поддержкой разрыва строкиа
            # Или дописывать части строки через оператор +=
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        # else избыточен, так как if уже содержит return
        else:
            return('Хватит есть!')


class CashCalculator(Calculator):
    # Достаточно формата 60. или 60.0 для указания
    # вещественного типа данных
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.
    # Так же названия переменных в данном случае
    # дают достаточно информации для опускания комментариев
    # хотя еще лучше было бы использовать EXCHANGE_RATE вместо просто RATE

    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        currency_type = currency
        # cash_remained по английски правильнее назвать
        # cash_remainders. Первый вариант в речи практически не
        # употребляется
        cash_remained = self.limit - self.get_today_stats()
        if currency == 'usd':
            cash_remained /= USD_RATE
            # операция сохранения currencyi_type в отдельную переменную
            # избыточная. И в целом такая проверка небезопасна
            # можно добавить дефолтный else либо использовать
            # тип данных вроде словаря
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            # В отличии от явного указания вещественного типа данных выше
            # в данном случае происходит его неявное указание
            # лучше придерживаться одного из вариантов
            cash_remained == 1.00
            # Ошибка
            # Лучше данную строчку просто опустить
            # либо явно прописать /= 1.0 (1.0 в данном случае эквивалентность
            # рубля к рублю)
            currency_type = 'руб'
            # В данном месте следовало оставить отступ для разбиения
            # логических частей кода
        if cash_remained > 0:
            # Скобки после return являются избыточными
            return (
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        elif cash_remained == 0:
            return 'Денег нет, держись'
        # elif в данном случае либо избыточен либо отсутствует
        # return для случая по умолчанию
        elif cash_remained < 0:
            # Комментарий к подобному виду return даны выше
            # Так же вместо смешниваний f-строк и метода .format
            # лучше остановиться на одном из вариантов. f-строки
            # поддерживают форматрование единообразно формату
            # операции над простыми строками вида :.2f
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)

    # Вызов данного метода является избыточным
    def get_week_stats(self):
        super().get_week_stats()
