import sample_data
import os

DATA_FILE_PATH = "./sample_data/question.csv"
DATA_HEADER = ['id', 'submisson_time', 'view_number', 'vote_number', 'title', 'message', 'image']


def get_all_questions():
    with open(DATA_FILE_PATH, "r") as file:
        lines = file.readlines()
    table = [element.replace("\n", "").split("|") for element in lines]
    return table


def write_user_story(question):
    with open(DATA_FILE_PATH, "w") as file:
        for story in question:
            row = '|'.join(story)
            file.write(row + "\n")


def add_question(added_line):
    table = get_all_questions()
    table.append(list(added_line.values()))
    write_user_story(table)