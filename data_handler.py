import sample_data
import os

DATA_FILE_PATH = "./sample_data/question.csv"
DATA_HEADER = ['id', 'submisson_time', 'view_number', 'vote_number', 'title', 'message', 'image']


def get_all_questions():
    with open(DATA_FILE_PATH, "r") as file:
        lines = file.readlines()
    table = [element.replace("\n", "").split("|") for element in lines]
    return table

