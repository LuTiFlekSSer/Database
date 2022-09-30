import random

bases = []
curr_bd = -1


def create_db(name: str):
    global curr_bd
    for x in bases:
        if x[0] == name:
            return -1
    bases.append([name, [], [], []])
    if curr_bd == -1:
        curr_bd = 0
    return 0


def add_student(full_name: str):
    global curr_bd
    name, surname, patronymic = full_name.strip().split(' ')
    if curr_bd != -1:
        bases[curr_bd][1].append([len(bases[curr_bd][1]), name, surname, patronymic])
        return 0
    return -1


def fill_students(path: str):
    global curr_bd
    if curr_bd != -1:
        try:
            file = open(path, 'r', encoding='UTF-8')
            for x in file:
                name, surname, patronymic = x.strip().split(' ')
                bases[curr_bd][1].append([len(bases[curr_bd][1]), name, surname, patronymic])
            file.close()
            return 0
        except FileNotFoundError:
            return -3
    return -1


def fill_tests(path: str):
    global curr_bd
    if curr_bd != -1:
        try:
            file = open(path, 'r', encoding='UTF-8')
            for x in file:
                add_test(x.strip())
            file.close()
            return 0
        except FileNotFoundError:
            return -3
    return -1


def add_test(path: str):
    global curr_bd
    if curr_bd != -1:
        for x in bases[curr_bd][2]:
            if path == x[1]:
                return -2
        bases[curr_bd][2].append([len(bases[curr_bd][2]), path])
        return 0
    return -1


def del_student(student_id: int):
    global curr_bd
    if curr_bd != -1:
        try:
            bases[curr_bd][1].pop(student_id)
            for x in range(student_id, len(bases[curr_bd][1])):
                bases[curr_bd][1][x][0] -= 1
            return 0
        except IndexError:
            return -3
    return -1


def del_test(test_id: int):
    global curr_bd
    if curr_bd != -1:
        try:
            bases[curr_bd][2].pop(test_id)
            for x in range(test_id, len(bases[curr_bd][2])):
                bases[curr_bd][2][x][0] -= 1
            return 0
        except IndexError:
            return -3
    return -1


def del_db(name: str):
    global curr_bd
    pos = -1
    for x in range(len(bases)):
        if name == bases[x][0]:
            pos = x
            break
    if pos != -1:
        if curr_bd == pos:
            curr_bd = -1
        elif curr_bd > pos:
            curr_bd -= 1
        bases.pop(pos)
        return 0
    return -1


def edit_student(student_id: int, new_full_name: str):
    global curr_bd
    name, surname, patronymic = new_full_name.split(' ')
    if curr_bd != -1:
        try:
            bases[curr_bd][1][student_id][1] = name
            bases[curr_bd][1][student_id][2] = surname
            bases[curr_bd][1][student_id][3] = patronymic
        except IndexError:
            return -3
        return 0
    return -1


def edit_test(test_id: int, new_path: str):
    global curr_bd
    if curr_bd != -1:
        try:
            for x in bases[curr_bd][2]:
                if new_path == x[1]:
                    return -2
            bases[curr_bd][2][test_id][1] = new_path
            return 0
        except IndexError:
            return -3
    return -1


def switch_bd(name: str):
    global curr_bd
    pos = -1
    for x in range(len(bases)):
        if bases[x][0] == name:
            pos = x
            break
    if pos != -1:
        curr_bd = pos
        return 0
    return -1


def create_testing_table():
    global curr_bd
    if curr_bd != -1:
        if len(bases[curr_bd][1]) != 0 and len(bases[curr_bd][2]) != 0:
            bases[curr_bd][3] = []
            for x in range(len(bases[curr_bd][1])):
                bases[curr_bd][3].append([x, random.randint(0, bases[curr_bd][2][-1][0])])
            return 0
        return -3
    return -1


def print_student(student_id: int):
    global curr_bd
    if curr_bd != -1:
        try:
            name = bases[curr_bd][1][student_id][1] + ' ' + bases[curr_bd][1][student_id][2] + ' ' + bases[curr_bd][1][student_id][3]
        except IndexError:
            return -3
        return name
    return -1


def print_test(test_id: int):
    global curr_bd
    if curr_bd != -1:
        try:
            name = bases[curr_bd][2][test_id][1]
        except IndexError:
            return -3
        return name
    return -1


def print_students_table():
    global curr_bd
    if curr_bd != -1:
        if len(bases[curr_bd][1]) != 0:
            for x in bases[curr_bd][1]:
                print('Full name:', x[1], x[2], x[3], 'ID:', x[0])
        else:
            print('No data')
        return 0
    return -1


def print_tests_table():
    global curr_bd
    if curr_bd != -1:
        if len(bases[curr_bd][2]) != 0:
            for x in bases[curr_bd][2]:
                print('Test:', x[1], 'ID:', x[0])
            return 0
        else:
            print('No data')
    return -1


def print_testing_table():
    global curr_bd
    if curr_bd != -1:
        if len(bases[curr_bd][3]) != 0:
            for x in bases[curr_bd][3]:
                print('Full name:', bases[curr_bd][1][x[0]][2], bases[curr_bd][1][x[0]][1], bases[curr_bd][1][x[0]][3], 'Test:',
                      bases[curr_bd][2][x[1]][1])
            return 0
        else:
            print('No data')
        return -3
    return -1


def save_db(name: str):
    pos = -1
    for x in range(len(bases)):
        if bases[x][0] == name:
            pos = x
    if pos != -1:
        file = open(name + '.txt', 'w', encoding='UTF-8')
        for x in bases[pos][1]:
            file.write(x[1] + ' ' + x[2] + ' ' + x[3] + '\n')
        file.write('<tests>\n')
        for x in bases[pos][2]:
            file.write(x[1] + '\n')
        file.write('<testing_table>\n')
        for x in bases[pos][3]:
            file.write(str(x[0]) + ' ' + str(x[1]) + '\n')
        file.close()
        return 0
    return -3


def load_db(name: str):
    global curr_bd
    try:
        file = open(name + '.txt', 'r', encoding='UTF-8')
        pos = -1
        for x in range(len(bases)):
            if bases[x][0] == name:
                pos = x
                break
        if pos == -1:
            bases.append(None)
            pos = len(bases) - 1
            if curr_bd == -1:
                curr_bd = pos
        bases[pos] = [name, [], [], []]
        for x in file:
            if x.strip() != '<tests>':
                name, surname, patronymic = x.strip().split(' ')
                bases[pos][1].append([len(bases[pos][1]), name, surname, patronymic])
            else:
                break
        for x in file:
            if x.strip() != '<testing_table>':
                bases[pos][2].append([len(bases[pos][2]), x.strip()])
            else:
                break
        for x in file:
            std_id, test_id = x.strip().split()
            bases[pos][3].append([int(std_id), int(test_id)])
        return 0
    except FileNotFoundError:
        return -1
