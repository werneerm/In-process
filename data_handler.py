import sample_data
import os
import connection
from psycopg2 import sql
import database_common

@connection.connection_handler
def get_all_question_sql(cursor):
    cursor.execute("""
                    SELECT * FROM question;
                   """,
                   )
    names = cursor.fetchall()
    return names

@connection.connection_handler
def get_top_question_sql(cursor):
    cursor.execute("""
                    SELECT * FROM question LIMIT 5;
                   """,
                   )
    names = cursor.fetchall()
    return names



@connection.connection_handler
def add_SQL_question(cursor, time, vote_num, view_num, title, message, image):

    cursor.execute("""
            INSERT INTO question (submission_time, view_number, vote_number, title, message, image)
            VALUES (TIMESTAMP %(time)s, %(vote_num)s, %(view_num)s, %(title)s, %(message)s, %(image)s);
            """, {'time': time, 'vote_num': vote_num, 'view_num': view_num, 'title': title, 'message': message,
                  'image': image})


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
def answer_update_SQL(cursor, message, image, id):
    cursor.execute("""
            UPDATE answer
            SET message=%(message)s, image=%(image)s
            WHERE id=%(id)s
            """, {'id': id, 'message': message, 'image': image})


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
def delete_SQL_question(cursor, ID):
    cursor.execute("""
            DELETE FROM question 
            WHERE  id=%(ID)s;
            """, {'ID': ID})

@connection.connection_handler
def delete_tags_of_question(cursor, ID):
    cursor.execute("""
        DELETE FROM question_tag
        WHERE question_id=%(ID)s;
    """, {'ID': ID})

@connection.connection_handler
def delete_SQL_answer(cursor, ID):
    cursor.execute("""
                DELETE FROM answer 
                WHERE  question_id=%(ID)s;
                """, {'ID': ID})

@connection.connection_handler
def delete_SQL_comment_with_question(cursor, ID):
    cursor.execute("""
                DELETE FROM comment 
                WHERE  question_id=%(ID)s;
                """, {'ID': ID})


@connection.connection_handler
def ID_from_SQL(cursor, title):  # szar
    cursor.execute("""
        SELECT id FROM question
        WHERE title=%(title)s
    """, {'title': title})
    ID = cursor.fetchall()
    return ID


@connection.connection_handler
def delete_SQL_question(cursor, ID):
    cursor.execute("""
            DELETE FROM question 
            WHERE  id=%(ID)s;
            """, {'ID': ID})

@connection.connection_handler
def delete_SQL_question_and_its_answer(cursor, ID):
    cursor.execute("""
            DELETE FROM answer 
            WHERE question_id=%(ID)s;
            """, {'ID': ID})


@connection.connection_handler
def delete_SQL_answer(cursor, ID):
    cursor.execute("""
                            DELETE FROM answer 
                            WHERE  question_id=%(ID)s;
                           """, {'ID': ID}
                   )

@connection.connection_handler
def upvote_questions_SQL(cursor, ID):
    cursor.execute("""
                            UPDATE question
                            SET vote_number = vote_number + 1
                            WHERE id=%(ID)s;
                              """, {'ID': ID}
                   )


@connection.connection_handler
def upvote_answers_SQL(cursor, ID):
    cursor.execute("""
                            UPDATE answer
                            SET vote_number = vote_number + 1
                            WHERE id=%(ID)s;
                              """, {'ID': ID}
                   )


@connection.connection_handler
def downvote_questions_SQL(cursor, ID):
    cursor.execute("""
                    UPDATE question
                    SET vote_number = vote_number - 1
                    WHERE id=%(ID)s;
                              """, {'ID': ID}
                   )


@connection.connection_handler
def downvote_answers_SQL(cursor, ID):
    cursor.execute("""
                            UPDATE answer
                            SET vote_number = vote_number - 1
                            WHERE id=%(ID)s;
                              """, {'ID': ID}
                   )


@connection.connection_handler
def sorting_sql(cursor, sort):
    cursor.execute(
        sql.SQL("""select * from question ORDER BY {} """)
            .format(sql.Identifier(sort)),
    )
    names = cursor.fetchall()
    return names


@connection.connection_handler
def sorting_sql_desc(cursor, dsort):
    cursor.execute(
        sql.SQL("""select * from question ORDER BY {} DESC""")
            .format(sql.Identifier(dsort)),
    )
    names = cursor.fetchall()
    return names


@connection.connection_handler
def search_title(cursor, question):
    cursor.execute("""
                            SELECT * from question
                            WHERE title ILIKE %(searched_word)s;
                              """,
                   {'searched_word': ("%" + question + "%")}
                   )
    result = cursor.fetchall()
    return result


@connection.connection_handler
def search_message(cursor, question):
    cursor.execute("""
                            SELECT * from question
                            WHERE message ILIKE %(searched_word)s;
                              """,
                   {'searched_word': ("%" + question + "%")}
                   )
    result = cursor.fetchall()
    return result


@connection.connection_handler
def answer_search_message(cursor, question):
    cursor.execute("""
                                SELECT * from answer
                                WHERE message ILIKE %(searched_word)s;
                                  """,
                   {'searched_word': ("%" + question + "%")})
    result = cursor.fetchall()
    return result



@connection.connection_handler
def get_all_tag(cursor):
    cursor.execute("""
                       SELECT * FROM tag;
                      """,
                   )
    names = cursor.fetchall()
    return names

@connection.connection_handler
def add_existing_tag(cursor,tag,question):
    cursor.execute("""
               INSERT INTO question_tag (question_id,tag_id)
               VALUES (%(question)s,%(tag)s);
               """,
                   {'question': question, 'tag': tag})

@connection.connection_handler
def question_tag(cursor):
    cursor.execute("""
                           SELECT * FROM question_tag;
                          """,
                   )
    names = cursor.fetchall()
    return names

@connection.connection_handler
def add_comment_to_Q(cursor, id, comment, time):
    cursor.execute("""
        INSERT INTO comment (question_id, answer_id, message, submission_time, edited_count)
        VALUES (%(id)s, NULL, %(comment)s,TIMESTAMP %(time)s, NULL)
    """, {'id': id, 'comment': comment, 'time': time})


@connection.connection_handler
def get_comment_for_Q(cursor, id):
    cursor.execute("""
        SELECT id, message, submission_time FROM comment
        WHERE question_id=%(id)s;
    """, {'id': id})
    comments = cursor.fetchall()
    return comments


@connection.connection_handler
def add_comment_to_A(cursor, id, comment, time):
    cursor.execute("""
        INSERT INTO comment (question_id, answer_id, message, submission_time, edited_count)
        VALUES (NULL, %(id)s, %(comment)s,TIMESTAMP %(time)s, NULL)
    """, {'id': id, 'comment': comment, 'time': time})


@connection.connection_handler
def get_comment_for_A(cursor, id):
    cursor.execute("""
        SELECT message, submission_time FROM comment
        WHERE answer_id=%(id)s;
    """, {'id': id})
    comments = cursor.fetchall()
    return comments

@connection.connection_handler
def get_answer_for_update(cursor, id):
    cursor.execute("""
        SELECT * FROM answer
        WHERE id=%(id)s;
    """, {'id': id})
    answer = cursor.fetchall()
    return answer

@connection.connection_handler
def delete_comment(cursor, id):
    cursor.execute("""
    DELETE FROM comment
    WHERE id=%(id)s
    """, {'id': id})

@connection.connection_handler
def get_comment_for_edit(cursor, id):
    cursor.execute("""
        SELECT id, message FROM comment
        WHERE id=%(id)s;
    """, {'id': id})
    comment = cursor.fetchall()
    return comment

@connection.connection_handler
def update_comment(cursor, comment, submission_time, id):
    cursor.execute("""
            UPDATE comment
            SET message=%(comment)s, submission_time=%(submission_time)s, edited_count=edited_count + 1
            WHERE id=%(id)s
    """, {'id': id, 'comment': comment, 'submission_time': submission_time})