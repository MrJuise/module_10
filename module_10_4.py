'''
Задача "Потоки гостей в кафе":
Необходимо имитировать ситуацию с посещением гостями кафе.
Создайте 3 класса: Table, Guest и Cafe.
Класс Table:

    Объекты этого класса должны создаваться следующим способом - Table(1)
    Обладать атрибутами number - номер стола и guest - гость, который сидит за этим столом (по умолчанию None)

Класс Guest:

    Должен наследоваться от класса Thread (быть потоком).
    Объекты этого класса должны создаваться следующим способом - Guest('Vasya').
    Обладать атрибутом name - имя гостя.
    Обладать методом run, где происходит ожидание случайным образом от 3 до 10 секунд.

Класс Cafe:

    Объекты этого класса должны создаваться следующим способом - Cafe(Table(1), Table(2),....)
    Обладать атрибутами queue - очередь (объект класса Queue) и tables - столы в этом кафе (любая коллекция).
    Обладать методами guest_arrival (прибытие гостей) и discuss_guests (обслужить гостей).

Метод guest_arrival(self, *guests):

    Должен принимать неограниченное кол-во гостей (объектов класса Guest).
    Далее, если есть свободный стол, то садить гостя за стол (назначать столу guest), запускать поток гостя
     и выводить на экран строку "<имя гостя> сел(-а) за стол номер <номер стола>".
    Если же свободных столов для посадки не осталось, то помещать гостя в очередь queue и выводить сообщение
     "<имя гостя> в очереди".

Метод discuss_guests(self):
Этот метод имитирует процесс обслуживания гостей.

    Обслуживание должно происходить пока очередь не пустая (метод empty) или хотя бы один стол занят.
    Если за столом есть гость(поток) и гость(поток) закончил приём пищи(поток завершил работу - метод is_alive),
     то вывести строки "<имя гостя за текущим столом> покушал(-а) и ушёл(ушла)" и "Стол номер <номер стола> свободен".
      Так же текущий стол освобождается (table.guest = None).
    Если очередь ещё не пуста (метод empty) и стол один из столов освободился (None), то текущему столу присваивается
    гость взятый из очереди (queue.get()). Далее выводится строка "<имя гостя из очереди> вышел(-ла) из очереди и сел(-а)
     за стол номер <номер стола>"
    Далее запустить поток этого гостя (start)

Таким образом мы получаем 3 класса на основе которых имитируется работа кафе:

    Table - стол, хранит информацию о находящемся за ним гостем (Guest).
    Guest - гость, поток, при запуске которого происходит задержка от 3 до 10 секунд.
    Cafe - кафе, в котором есть определённое кол-во столов и происходит имитация прибытия гостей (guest_arrival) и их
     обслуживания (discuss_guests).

'''
from threading import Thread
import random
from queue import Queue
import time

class Table:
    def __init__(self, number):
        self.number = number
        self.guest = None
class Guest(Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name
    def run(self):
        time.sleep(random.randint(3, 10))
class Cafe:
    def __init__(self, *tables):
        self.queue = Queue()                         # Создаёт очередь для гостей, ожидающих стол.
        self.tables = tables
    def guest_arrival(self, *guests):
        for guest in guests:                         # Итерируется по каждому гостю.
            for table in self.tables:                # Итерирует по всем столам в кафе.
                if table.guest is None:              # Проверяет, свободен ли стол
                    table.guest = guest              # Если стол свободен, гость сажается за него.
                    guest.start()                    # Запускает поток для данного гостя.
                    print(f'{guest.name} сел(а) за стол номер {table.number}')
                    break
            else:                                    # Если мест нет.
                self.queue.put(guest)                # Добавляет гостя в очередь.
                print(f'{guest.name} в очереди.')
    def discuss_guests(self):
        while True:                                  # Бесконечный цикл, который будет продолжаться, пока есть гости и очередь.
            s = False                                # Переменная, чтобы отслеживать, были ли освобождены столы.
            for table in self.tables:                # Итерирует по каждой столу.
                if table.guest is not None:          # Проверяет, есть ли гость за столом.
                    if not table.guest.is_alive():   # Проверяет, завершился ли поток
                        print(f'{table.guest.name} покушал(-а) и ушёл(ушла)')
                        table.guest = None           # Освобождает стол, устанавливая его снова в состояние `None`.
                        print(f'Стол номер {table.number} свободен')
                        s = True
            if s:                                    # Если освободили хотя бы один стол.
                if not self.queue.empty():           # Если в очереди есть гость.
                    next_guest = self.queue.get()    # Извлекаем следующего гостя из очереди.
                    for table in self.tables:        # Ищем свободный стол для следующего гостя.
                        if table.guest is None:      # Проверяет, свободен ли стол.
                            table.guest = next_guest # Сажает следующего гостя за стол.
                            next_guest.start()       # Запускает поток для следующего гостя.
                            print(f'{next_guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}')
                            break
            if self.queue.empty() and all(table.guest is None for table in self.tables):   # Проверка, если в очереди нет гостей и все столы свободны
                break                               # Если да, то выход из бесконечного цикла



tables = [Table(number) for number in range(1, 6)]
# Имена гостей
guests_names = [
'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]
# Создание гостей
guests = [Guest(name) for name in guests_names]
# Заполнение кафе столами
cafe = Cafe(*tables)
# Приём гостей
cafe.guest_arrival(*guests)
# Обслуживание гостей
cafe.discuss_guests()









