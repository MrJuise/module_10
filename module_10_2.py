'''
Задача "За честь и отвагу!":
Создайте класс Knight, наследованный от Thread, объекты которого будут обладать следующими свойствами:

    Атрибут name - имя рыцаря. (str)
    Атрибут power - сила рыцаря. (int)

А также метод run, в котором рыцарь будет сражаться с врагами:

    При запуске потока должна выводится надпись "<Имя рыцаря>, на нас напали!".
    Рыцарь сражается до тех пор, пока не повергнет всех врагов (у всех потоков их 100).
    В процессе сражения количество врагов уменьшается на power текущего рыцаря.
    По прошествию 1 дня сражения (1 секунды) выводится строка "<Имя рыцаря> сражается <кол-во дней>..., осталось <кол-во воинов> воинов."
    После победы над всеми врагами выводится надпись "<Имя рыцаря> одержал победу спустя <кол-во дней> дней(дня)!"

'''

from threading import Thread
from time import sleep

class Knight(Thread):
    def __init__(self, name, power):
        super().__init__()
        self.name = name
        self.power = power
        self.enemies = 100
    def run(self):
        print(f'{self.name}, на нас напали!')
        day = 0
        while self.enemies > 0:
            sleep(1)
            day += 1
            self.enemies -= self.power
            print(f'{self.name}, сражается {day} дней, осталось {self.enemies} воинов')
        if self.enemies <= 0:
            print(f'{self.name} одержал победу спустя {day} дней')

first_knight = Knight('Sir Lancelot', 10)
second_knight = Knight("Sir Galahad", 20)

first_knight.start()
second_knight.start()

first_knight.join()
second_knight.join()
