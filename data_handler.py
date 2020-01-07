import sample_data
import os

DATA_FILE_PATH = "./sample_data/question.csv"
DATA_HEADER = ['id', 'submisson_time', 'view_number', 'vote_number', 'title', 'message', 'image']


def get_all_questions():
    with open(DATA_FILE_PATH, "r") as file:
        lines = file.readlines()
    table = [element.replace("\n", "").split(";") for element in lines]
    question_dict = { i : table[i] for i in range(0, len(table) ) }
    return table

def question_dict(table):
    question_dict = {i: table[i] for i in range(0, len(table))}
    return question_dict



def write_user_story(question):
    with open(DATA_FILE_PATH, "w") as file:
        for story in question:
            row = '|'.join(story)
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
    #final_answer =
    for i in answer :
        if i[3] == str(ID):
            return i[4]
