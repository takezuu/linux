import subprocess
import csv
import time
import os


def data():
    # Получаем информацию из терминала
    output = subprocess.check_output(['ps', 'aux', '--sort', '-%mem'], encoding='utf-8')
    data = output.split('\n')
    headers = data[0].split()

    # Создаем CSV файл с данными из терминала
    with open('data.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(headers)
        for i in data[1:]:
            row = i.split()
            writer.writerow(row)


def open_report_file():
    timestr = time.strftime("%d-%m-%Y-%H_%M")
    file = open(f'{timestr}-scan.txt', 'w')
    file.write("Отчёт о состоянии системы:\n")
    file.close()
    return f'{timestr}-scan.txt'


def add_to_report_file(text, file_name):
    file = open(f'{file_name}', 'a')
    file.write(text)
    file.close()


def all_processes(file_name):
    csv_file = open("data.csv")
    reader = csv.reader(csv_file)
    processes = len(list(reader)) - 1
    text_processes = f"Процессов запущено: {processes}\n"
    add_to_report_file(text_processes, file_name)


def get_system_users():
    csv_file = open("data.csv")
    data = list(csv.reader(csv_file))
    users = []
    for i in data[1:-1]:
        if i[0] not in users:
            users.append(i[0])
    return users


def write_system_users(users,file_name):
    output = "Пользователи системы:\n"
    for i in users:
        i = str(i)
        output += f"'{i}',"
    output = output[:-1]
    add_to_report_file(output+'\n', file_name)


def get_amount_of_users_processes(users):
    csv_file = open("data.csv")
    data = list(csv.reader(csv_file))
    nums = []
    for user in users:
        num = 0
        for i in data[1:]:
            num += (i.count(user))
        nums.append(num)
    amount_of_processes = dict(zip(users, nums))
    return amount_of_processes


def write_amount_of_users_processes(data, file_name):
    file = open(f'{file_name}', 'a')
    file.write("Пользовательских процессов:\n")
    for k, v in data.items():
        file.write(f"{k}:{v}\n")
    file.close()


def get_memory_in_use(file_name):
    output = subprocess.check_output(['free', '-m'], encoding='utf-8')
    data = output.split('\n')
    memory = data[1].split()
    memory_text = f"Всего памяти используется: {memory[2]} mb\n"
    add_to_report_file(memory_text, file_name)


def get_cpu_info(file_name):
    csv_file = open("data.csv")
    data = list(csv.reader(csv_file))
    cpu = 0
    for i in data[1:-1]:
        cpu += float(i[2])
    cpu_text = f"Всего CPU используется: {round(cpu, 1)}%\n"
    add_to_report_file(cpu_text, file_name)


def get_max_memory(file_name):
    csv_file = open("data.csv")
    data = list(csv.reader(csv_file))
    memory_text = f"Больше всего памяти использует: {data[1][10][:20]}\n"
    add_to_report_file(memory_text, file_name)


def get_max_cpu(file_name):
    output = subprocess.check_output(['ps', 'aux', '--sort', '-%cpu'], encoding='utf-8')
    data = output.split('\n')
    max_cpu_string = data[1].split()
    max_cpu_text = f"Больше всего CPU использует: {max_cpu_string[10][:20]}\n"
    add_to_report_file(max_cpu_text, file_name)


def print_report(file_name):
    with open(f'{file_name}', 'r') as file:
        for line in file:
            print(line[:-1])


def delete_data():
    os.remove('data.csv')

if __name__ == '__main__':
    data()
    #Получаем уникальных пользователей
    users = get_system_users()
    #Создаем текстовый отчет"
    file_name = open_report_file()
    #Записываем кол-во всех процессов"
    all_processes(file_name)
    #Записываем пользователей в отчет"
    write_system_users(users, file_name)
    #Формируем словарь с кол-вом процессов пользователей
    dict_of_amount_of_processes = get_amount_of_users_processes(users)
    #Записываю кол-во процессов у каждого пользователя
    write_amount_of_users_processes(dict_of_amount_of_processes, file_name)
    #Записываю сколько используетс памяти
    get_memory_in_use(file_name)
    #Записываю загруженность процессора
    get_cpu_info(file_name)
    #Записываю процесс с максимальной памятью
    get_max_memory(file_name)
    #Записываю процесс с максимальной нагрузкой на процессор
    get_max_cpu(file_name)
    print_report(file_name)
    delete_data()
