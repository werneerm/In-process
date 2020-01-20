import sample_data
import os
import connection
import psycopg2
import psycopg2.extras

DATA_FILE_PATH = "./sample_data/question.csv"
DATA_HEADER = ['id', 'submisson_time', 'view_number', 'vote_number', 'title', 'message', 'image']


def get_all_questions():
    with open(DATA_FILE_PATH, "r") as file:
        lines = file.readlines()
    table = [element.replace("\n", "").split(";") for element in lines]
    return table

def question_dict(table):
    question_dict = {i: table[i] for i in range(0, len(table))}
    return question_dict



def write_user_story(file_path, data):
    with open(file_path, "w") as file:
        for record in data:
            row = ';'.join(record)
            file.write(row + "\n")


def add_question(added_line):
    table = get_all_questions()
    table.append(list(added_line.values()))
    write_user_story(table)

def get_all_answer():
    with open('./sample_data/answer.csv', "r") as file:
        lines = file.readlines()
    table = [element.replace("\n", "").split(";") for element in lines]
    question_dict = {i: table[i] for i in range(0, len(table))}
    return table

def index_finder(ID):
    answer = get_all_answer()
    final_answer = []
    for i in answer:
        if i[3] == str(ID):
            final_answer.append(i)
    return final_answer

def id_generator(table):
    old_id = table[-1][0]
    new_id = int(old_id) + 1
    return str(new_id)

def question_finder(ID):
    quests = get_all_questions()
    the_question = ""
    the_message = ""
    the_image = ""
    for i in quests:
        if i[0] == str(ID):
            the_question = i[4]
            the_message = i[5]
            # the_image = i[6]
    return the_question, the_message, the_image

def question_change(title, message, image, table, id):
    for line in table:
        if line[0] == str(id):
            line[4] = title
            line[5] = message
            line[6] = image
    write_user_story('./sample_data/question.csv', table)

def delete_question(id, table, answers):
    answers_to_delete = []
    for line in table:
        if line[0] == str(id):
            table.remove(line)
    for line in answers:
        if str(id) == line[3]:
            answers_to_delete.append(line)
    for item in answers_to_delete:
        answers.remove(item)
    write_user_story("./sample_data/question.csv",table)
    write_user_story("./sample_data/answer.csv", answers)


def delete_answer(id, table,):
    question_id = ""
    for line in table:
        if str(line[0]) == str(id):
            question_id = line[3]
            table.remove(line)
    write_user_story("./sample_data/answer.csv", table)
    return question_id

def sorting_things(sorted_item):
    table =  get_all_questions()
    index = DATA_HEADER.index(sorted_item)
    l = len(table)
    if sorted_item == 'message' or sorted_item == 'title':
        for i in range(0, l):
            for j in range(0, l - i - 1):
                if (table[j][index] > table[j + 1][index]):
                    tempo = table[j]
                    table[j] = table[j + 1]
                    table[j + 1] = tempo
        return table
    elif sorted_item == 'id' or 'submisson_time' or 'view_number' or 'vote_number':
        for i in range(0, l):
            for j in range(0, l - i - 1):
                if (int(table[j][index]) > int(table[j + 1][index])):
                    tempo = table[j]
                    table[j] = table[j + 1]
                    table[j + 1] = tempo
        return table
@connection.connection_handler
def get_all(cursor):
    cursor.execute("""
        SELECT * FROM question
    """)
    data = cursor.fetchall()
    return data