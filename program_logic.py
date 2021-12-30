import random
import copy


def get_numbers_from_index(row, column):
    return row * 4 + column + 1


def pretty_print(mas):
    print("-" * 10)
    for row in mas:
        print(*row)
    print("-" * 10)


def get_index_for_number(num):
    num -= 1
    x, y = num // 4, num % 4
    return x, y


def insert_2_or_4(mas, x, y):
    if random.random() >= 0.75:
        mas[x][y] = 4
    else:
        mas[x][y] = 2
    return mas


def get_empty_list(mas):
    empty = []
    for row in range(0, 4):
        for column in range(0, 4):
            if mas[row][column] == 0:
                num = get_numbers_from_index(row, column)
                empty.append(num)
    return empty


def is_zero_in_mas(mas):
    for row in mas:
        if 0 in row:
            return True
    return False


def move_left(mas):
    delta = 0
    origin = copy.deepcopy(mas)
    for row in mas:
        while 0 in row:
            row.remove(0)
        while len(row) != 4:
            row.append(0)
    for i in range(4):
        for j in range(3):
            if mas[i][j] == mas[i][j + 1] and mas[i][j] != 0:
                mas[i][j] *= 2
                delta += mas[i][j]
                mas[i].pop(j + 1)
                mas[i].append(0)
    return mas, delta, not origin == mas


def move_right(mas):
    delta = 0
    origin = copy.deepcopy(mas)
    for row in mas:
        while 0 in row:
            row.remove(0)
        while len(row) != 4:
            row.insert(0, 0)
    for i in range(4):
        for j in range(3, 0, -1):
            if mas[i][j] == mas[i][j - 1] and mas[i][j] != 0:
                mas[i][j] *= 2
                delta += mas[i][j]
                mas[i].pop(j - 1)
                mas[i].insert(0, 0)
    return mas, delta, not origin == mas


def move_up(mas):
    delta = 0
    origin = copy.deepcopy(mas)
    for i_2 in range(2):
        for j_2 in range(4):
            if mas[i_2 + 1][j_2] == 0 and mas[i_2 + 2][j_2] != 0:
                mas[i_2 + 1][j_2] = mas[i_2 + 2][j_2]
                mas[i_2 + 2][j_2] = 0
            if mas[i_2][j_2] == 0:
                mas[i_2][j_2] = mas[i_2 + 1][j_2]
                mas[i_2 + 1][j_2] = 0
    for row in range(3):
        for column in range(4):
            if mas[row][column] == mas[row + 1][column]:
                mas[row][column] *= 2
                delta += mas[row][column]
                mas[row + 1][column] = 0
    for i in range(2):
        for j in range(4):
            if mas[i + 1][j] == 0 and mas[i + 2][j] != 0:
                mas[i + 1][j] = mas[i + 2][j]
                mas[i + 2][j] = 0
            if mas[i][j] == 0:
                mas[i][j] = mas[i + 1][j]
                mas[i + 1][j] = 0
    return mas, delta, not origin == mas


def move_down(mas):
    delta = 0
    origin = copy.deepcopy(mas)
    for i_2 in range(4, 1, -1):
        for j_2 in range(4):
            if mas[i_2 - 1][j_2] == 0 and mas[i_2 - 2][j_2] != 0:
                mas[i_2 - 1][j_2] = mas[i_2 - 2][j_2]
                mas[i_2 - 2][j_2] = 0
    for i_3 in range(4, 1, -1):
        for j_3 in range(4):
            if mas[i_3 - 1][j_3] == 0 and mas[i_3 - 2][j_3] != 0:
                mas[i_3 - 1][j_3] = mas[i_3 - 2][j_3]
                mas[i_3 - 2][j_3] = 0
    for row in range(4, 1, -1):
        for column in range(4):
            if mas[row - 1][column] == mas[row - 2][column]:
                mas[row - 1][column] *= 2
                delta += mas[row - 1][column]
                mas[row - 2][column] = 0
    for i in range(4, 1, -1):
        for j in range(4):
            if mas[i - 1][j] == 0 and mas[i - 2][j] != 0:
                mas[i - 1][j] = mas[i - 2][j]
                mas[i - 2][j] = 0
    return mas, delta, not origin == mas


def can_move(mas):
    one = copy.deepcopy(mas)
    two = copy.deepcopy(mas)
    three = copy.deepcopy(mas)
    four = copy.deepcopy(mas)
    x, y, trash = move_right(one)
    t, b, trash = move_left(two)
    g, h, trash = move_up(three)
    n, v, trash = move_down(four)
    if mas == x and mas == t and mas == g and mas == n:
        return False
    else:
        return True
