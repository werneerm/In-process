import sample_data
import os
import connection
from psycopg2 import sql
import database_common

DATA_FILE_PATH = "./sample_data/question.csv"
DATA_HEADER = ['id', 'submisson_time', 'view_number', 'vote_number', 'title', 'message', 'image']

@connection.connection_handler
def get_all_question_sql(cursor):
    cursor.execute("""
                    SELECT * FROM question;
                   """,
                   )
    names = cursor.fetchall()
    return names

def index_finder(ID):
    answer = get_all_answer()
    final_answer = []
    for i in answer:
        if i[3] == str(ID):
            final_answer.append(i)
    return final_answer

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
def add_SQL_question(cursor, time, vote_num, view_num, title, message, image):

    cursor.execute("""
            INSERT INTO question (submission_time, view_number, vote_number, title, message, image)
            VALUES (TIMESTAMP %(time)s, %(vote_num)s, %(view_num)s, %(title)s, %(message)s, %(image)s);
            """, {'time': time, 'vote_num': vote_num, 'view_num': view_num, 'title': title, 'message': message, 'image': image})
@connection.connection_handler
def get_question_SQL(cursor, id):
    cursor.execute("""
    SELECT * FROM question
    WHERE id=%(id)s;
    """, {'id': id})
    question = cursor.fetchall()
    return question
@connection.connection_handler
def get_answer_for_question_SQL(cursor, id):
    cursor.execute("""
        SELECT * FROM answer
        WHERE question_id=%(id)s;
    """, {'id': id})
    answer = cursor.fetchall()
    return answer

@connection.connection_handler
def question_update_SQL(cursor, title, message, image, id):
    cursor.execute("""
            UPDATE question
            SET title=%(title)s, message=%(message)s, image=%(image)s
            WHERE id=%(id)s
    """, {'id': id, 'title': title, 'message': message, 'image': image})
@connection.connection_handler
def question_finder_SQL(cursor, id):
    cursor.execute("""
            SELECT title, message, image FROM question
            WHERE id=%(id)s
    """, {'id': id})
    row = cursor.fetchall()
    return row
@connection.connection_handler
def add_answer_SQL(cursor, time, vote_num, question_id, message, image):
    cursor.execute("""
            INSERT INTO answer (submission_time, vote_number, question_id, message, image)
            VALUES (TIMESTAMP %(time)s, %(vote_num)s, %(question_id)s, %(message)s, %(image)s);
            """, {'time': time, 'vote_num': vote_num, 'question_id': question_id, 'message': message, 'image': image})

@connection.connection_handler
def delete_SQL_question(cursor,ID):
    cursor.execute("""
            DELETE FROM question 
            WHERE  id=%(ID)s;
            """,{'ID':ID})

@connection.connection_handler
def delete_SQL_answer(cursor,ID):
    cursor.execute("""
                DELETE FROM answer 
                WHERE  question_id=%(ID)s;
                """,{'ID':ID})
@connection.connection_handler
def ID_from_SQL(cursor, title): #szar
    cursor.execute("""
        SELECT id FROM question
        WHERE title=%(title)s
    """, {'title': title})
    ID = cursor.fetchone()
    return ID
@connection.connection_handler
def delete_SQL_question(cursor,ID):
    cursor.execute("""
            DELETE FROM question 
            WHERE  id=%(ID)s;
            """,{'ID':ID}
                   )


@connection.connection_handler
def delete_SQL_answer(cursor,ID):
    cursor.execute("""
                            DELETE FROM answer 
                            WHERE  id=%(ID)s;
                           """,{'ID':ID}
                   )
@connection.connection_handler
def upvote_questions_SQL(cursor,ID):
    cursor.execute("""
                            UPDATE question 
                            SET vote_number = vote_number + 1
                            WHERE id=%(ID)s;
                              """, {'ID': ID}
                   )
@connection.connection_handler
def upvote_answers_SQL(cursor,ID):
    cursor.execute("""
                            UPDATE answer 
                            SET vote_number = vote_number + 1
                            WHERE id=%(ID)s;
                              """, {'ID': ID}
                   )

@connection.connection_handler
def downvote_questions_SQL(cursor,ID):
    cursor.execute("""
                            UPDATE question 
                            SET vote_number = vote_number - 1
                            WHERE id=%(ID)s;
                              """, {'ID': ID}
                   )

@connection.connection_handler
def downvote_answers_SQL(cursor,ID):
    cursor.execute("""
                            UPDATE answer 
                            SET vote_number = vote_number - 1
                            WHERE id=%(ID)s;
                              """, {'ID': ID}
                   )