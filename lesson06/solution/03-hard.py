# Задание-1: Решите задачу (дублированную ниже):

# Дана ведомость расчета заработной платы (файл "data/workers").
# Рассчитайте зарплату всех работников, зная что они получат полный оклад,
# если отработают норму часов. Если же они отработали меньше нормы,
# то их ЗП уменьшается пропорционально, а за заждый час переработки они получают
# удвоенную ЗП, пропорциональную норме.
# Кол-во часов, которые были отработаны, указаны в файле "data/hours_of"

# С использованием классов.
# Реализуйте классы сотрудников так, чтобы на вход функции-конструктора
# каждый работник получал строку из файла


class Worker:
    __first_name = ''
    __last_name = ''

    salary = 0
    job_title = ''
    hours_normal = 0
    hours_completed = 0

    @property
    def first_name(self):
        return self.__first_name

    @property
    def last_name(self):
        return self.__last_name

    @property
    def fullname(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def total_salary(self):
        hour_cost = self.salary / self.hours_normal

        if self.hours_completed > self.hours_normal:
            overworked = self.hours_completed - self.hours_normal
            total = self.salary + ((hour_cost * 2) * overworked)
        elif self.hours_completed < self.hours_normal:
            uncompleted = self.hours_normal - self.hours_completed
            total = self.salary - (hour_cost * uncompleted)
        else:
            total = self.salary

        return round(total, 2)

    def __init__(self, file_line: str):
        props = file_line.split()

        self.__first_name = props[0]
        self.__last_name = props[1]

        self.salary = int(props[2])
        self.job_title = props[3]
        self.hours_normal = int(props[4])

    def __str__(self):
        return f'Worker: {self.fullname}, Job: {self.job_title}, Salary: {self.salary}, Total: {self.total_salary}'


# Create empty list for workers
workers = []
completed = []

# Get files content and instantiate workers
with open('lesson06/solution/data/workers') as f:
    workers_list = f.readlines()[1:]

    for line in workers_list:
        workers.append(Worker(line))

with open('lesson06/solution/data/hours_of') as f:
    hours_list = f.readlines()[1:]

    for line in hours_list:
        dict_keys = ['first_name', 'last_name', 'completed']
        dict_values = line.split()

        item = dict(zip(dict_keys, dict_values))
        item['completed'] = int(item['completed'])

        completed.append(item)

# Show information about each worker
for person in workers:
    for item in completed:
        if item['first_name'] == person.first_name and item['last_name'] == person.last_name:
            person.hours_completed = item['completed']

    print(person)
