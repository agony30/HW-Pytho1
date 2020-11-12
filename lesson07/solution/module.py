import random


# строка карточки
class CardRow:
    _numbers: list

    @property
    def numbers(self):
        return self._numbers

    @numbers.setter
    def numbers(self, numbers: list):
        if len(numbers) != 5:
            raise ValueError
        else:
            self._numbers = []

            for x in numbers:
                self._numbers.append(x)  # или копировать список

            self._numbers.sort()  # 0 -> 9

            while len(self._numbers) < 9:
                random_index = random.randint(0, len(self._numbers))
                self._numbers.insert(random_index, '__')  # вместо пустых мест

    def check_number(self, value):
        if value in self._numbers:
            index = self._numbers.index(value)
            self._numbers[index] = '--'

            return True
        else:
            return False

    def __init__(self, numbers):
        self.numbers = numbers

    def __str__(self):
        num_list = list(map(str, self.numbers))
        num_list = [x.rjust(2) for x in num_list]
        result_str = "-".join(num_list)

        return result_str

    def __repr__(self):
        return self.__str__()


# карточка
class Card:
    _rows: list

    def __init__(self):
        random_numbers = random.sample(range(1, 90 + 1), k=15)
        self.rows = random_numbers

    def __str__(self):
        return self.rows

    def is_number_exists(self, number):
        for row in self._rows:
            if number in row.numbers:
                return True
        else:
            return False

    def check_number(self, number):
        for row in self._rows:
            if number in row.numbers:
                row.check_number(number)

    @property
    def rows(self):
        return "\n".join([str(row) for row in self._rows])

    @rows.setter
    def rows(self, numbers):
        self._rows = []

        number_step = 0

        for _ in range(3):
            self._rows.append(CardRow(numbers[number_step:number_step + 5]))
            number_step += 5

    @property
    def is_completed(self):
        status = True

        for row in self._rows:
            only_integer_values = list(filter(
                lambda x: isinstance(x, int),
                row.numbers
            ))  # --, __, -

            if len(only_integer_values) > 0:
                status = False

        return status


# итератор бочонков
class BoxIterator:
    _box_index: int
    boxes: list
    active: bool = True

    def __init__(self, count=90):
        self.boxes = [x for x in range(1, count + 1)]
        self._box_index = -1

        random.shuffle(self.boxes)

    def __iter__(self):
        return self

    def __next__(self):
        if self.active and self._box_index < len(self.boxes) - 1:
            self._box_index += 1
            print(f"Boxes remain: {len(self.boxes) - self._box_index}")

            return self.boxes[self._box_index]
        else:
            raise StopIteration


# игрок
class Player:
    name: str
    card: Card

    def __init__(self, name: str, card: Card):
        self.name = name
        self.card = card

    def __str__(self):
        return f"{'_' * 20}\nPlayer: {self.name}\nCard: \n{self.card}"

    def __repr__(self):
        return f"\n{self.__str__()}\n"


# игровой менеджер
class GameManager:
    players: list
    _iterator: BoxIterator

    def __init__(self):
        self._iterator = BoxIterator()

    def __game_loop(self):
        for box in self._iterator:
            print(self.players[0])
            print(self.players[1])

            print(f"\nBox number is ___{box}___")

            self.user_action(box)
            self.computer_action(box)

    def start(self):
        print("Loto game - v0.1 alpha\n\n")

        username = input('Type username: ')

        self.players = [
            Player(username, Card()),
            Player('computer', Card())
        ]

        self.__game_loop()

    def looser(self, user: Player):
        self._iterator.active = False
        print(f"User {user.name} loose!")

    def winner(self, user: Player):
        self._iterator.active = False
        print(f"User {user.name} win!")

    def user_action(self, box_number: int):
        command = input("What You want to do? [N - Next / C - Check] ")[0].lower()
        user = self.players[0]

        if command == 'n':
            if user.card.is_number_exists(box_number):
                self.looser(user)
        elif command == 'c':
            if user.card.is_number_exists(box_number):
                user.card.check_number(box_number)

                if user.card.is_completed:
                    self.winner(user)
            else:
                self.looser(user)
        else:
            print("Invalid command, try again!")
            self.user_action(box_number)

    def computer_action(self, box_number: int):
        user = self.players[1]

        if user.card.is_number_exists(box_number):
            user.card.check_number(box_number)

            if user.card.is_completed:
                self.winner(user)
