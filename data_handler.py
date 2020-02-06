import sample_data
import os
import connection
from psycopg2 import sql
import database_common
import sever
import psycopg2
import bcrypt

@connection.connection_handler
def get_all_question_sql(cursor):
    cursor.execute("""
                    SELECT * FROM question
                    ORDER BY id;
                   """,
                   )
    names = cursor.fetchall()
    return names

@connection.connection_handler
def get_top_question_sql(cursor):
    cursor.execute("""
                    SELECT * FROM question
                     ORDER BY id LIMIT 5;
                   """,)
    names = cursor.fetchall()
    return names



@connection.connection_handler
def add_SQL_question(cursor, time, vote_num, view_num, title, message, image, owner):

    cursor.execute("""
            INSERT INTO question (submission_time, view_number, vote_number, title, message, image, owner)
            VALUES (TIMESTAMP %(time)s, %(view_num)s, %(vote_num)s, %(title)s, %(message)s, %(image)s, %(owner)s);
            """, {'time': time, 'vote_num': vote_num, 'view_num': view_num, 'title': title, 'message': message,
                  'image': image, 'owner': owner})


@connection.connection_handler
def get_question_SQL(cursor, id):
    cursor.execute("""
    SELECT * FROM question
    WHERE id=%(id)s
    ORDER BY id;
    """, {'id': id})
    question = cursor.fetchall()
    return question


@connection.connection_handler
def get_answer_for_question_SQL(cursor, id):
    cursor.execute("""
        SELECT * FROM answer
        WHERE question_id=%(id)s
        ORDER BY id;
    """, {'id': id})
    answer = cursor.fetchall()
    return answer

@connection.connection_handler
def get_answer_for_question_SQL_with_ans_id(cursor, id):
    cursor.execute("""
        SELECT * FROM answer
        WHERE id=%(id)s
        ORDER BY id;
    """, {'id': id})
    answer = cursor.fetchall()
    return answer


@connection.connection_handler
def question_update_SQL(cursor, title, message, image, id,owner):
    cursor.execute("""
            UPDATE question
            SET title=%(title)s, message=%(message)s, image=%(image)s,owner=%(owner)s
            WHERE id=%(id)s
    """, {'id': id, 'title': title, 'message': message, 'image': image,'owner':owner})

@connection.connection_handler
def answer_update_SQL(cursor, message, image, id,owner):
    cursor.execute("""
            UPDATE answer
            SET message=%(message)s, image=%(image)s,owner=%(owner)s
            WHERE id=%(id)s
            """, {'id': id, 'message': message, 'image': image,'owner':owner})


@connection.connection_handler
def question_finder_SQL(cursor, id):
    cursor.execute("""
            SELECT title, message, image FROM question
            WHERE id=%(id)s
    """, {'id': id})
    row = cursor.fetchall()
    return row


@connection.connection_handler
def add_answer_SQL(cursor, time, vote_num, question_id, message, image, owner):
    cursor.execute("""
            INSERT INTO answer (submission_time, vote_number, question_id, message, image, owner)
            VALUES (TIMESTAMP %(time)s, %(vote_num)s, %(question_id)s, %(message)s, %(image)s, %(owner)s);
            """, {'time': time, 'vote_num': vote_num, 'question_id': question_id, 'message': message, 'image': image, 'owner': owner})


@connection.connection_handler
def delete_SQL_question(cursor, ID,owner):
    cursor.execute("""
            DELETE FROM question 
            WHERE  id=%(ID)s and owner = %(owner)s;
            """, {'ID': ID , 'owner':owner})

@connection.connection_handler
def delete_tags_of_question(cursor, ID,owner):
    cursor.execute("""
        DELETE FROM question_tag
        WHERE question_id=%(ID)s ;
    """, {'ID': ID})

@connection.connection_handler
def delete_SQL_answer(cursor, ID, owner):
    cursor.execute("""
                DELETE FROM answer 
                WHERE  question_id=%(ID)s and owner=%(owner)s;
                """, {'ID': ID,'owner':owner})

@connection.connection_handler
def delete_SQL_comment_with_question(cursor, ID,owner):
    cursor.execute("""
                DELETE FROM comment 
                WHERE  question_id=%(ID)s and owner=%(owner)s;
                """, {'ID': ID,'owner':owner})


# @connection.connection_handler
# def ID_from_SQL(cursor, title):  # szar
#     cursor.execute("""
#         SELECT id FROM question
#         WHERE title=%(title)s
#     """, {'title': title})
#     ID = cursor.fetchall()
#     return ID


@connection.connection_handler
def delete_SQL_question(cursor, ID,user):
    cursor.execute("""
                DELETE FROM answer
                WHERE question_id=%(ID)s ;
                DELETE FROM comment
                WHERE question_id=%(ID)s;
                DELETE FROM question_tag
                WHERE question_id=%(ID)s;
                DELETE FROM question
                WHERE  id=%(ID)s;
            """, {'ID': ID,'user':user})

@connection.connection_handler
def delete_SQL_question_and_its_answer(cursor, ID,owner):
    cursor.execute("""
            DELETE FROM answer 
            WHERE question_id=%(ID)s and owner=%(owner)s;
            """, {'ID': ID,'owner':owner})

#
# @connection.connection_handler
# def delete_SQL_answer(cursor, ID):
#     cursor.execute("""
#                             DELETE FROM answer
#                             WHERE  question_id=%(ID)s;
#                            """, {'ID': ID}
#                    )
@connection.connection_handler
def delete_question_tag(cursor, id):
    cursor.execute("""
        DELETE FROM question_tag
        WHERE question_id=%(id)s;
    """, {'id': id})
@connection.connection_handler
def delete_answer_comment(cursor, id,owner):
    cursor. execute("""
    DELETE FROM comment
    WHERE answer_id = %(id)s and owner=%(owner)s;
    """, {'answer_id': id,'owner':owner})

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
   try:
           cursor.execute("""
                   INSERT INTO question_tag (question_id,tag_id)
                   VALUES (%(question)s,%(tag)s);
                   """,
                       {'question': question, 'tag': tag})

   except psycopg2.errors.lookup("23505"):
       return sever.sever_error()


@connection.connection_handler
def question_tag(cursor):
    cursor.execute("""
                           SELECT * FROM question_tag;
                          """,
                   )
    names = cursor.fetchall()
    return names

@connection.connection_handler
def add_comment_to_Q(cursor, id, comment, time,owner):
    cursor.execute("""
        INSERT INTO comment (question_id, answer_id, message, submission_time, edited_count,owner)
        VALUES (%(id)s, NULL, %(comment)s,TIMESTAMP %(time)s, NULL,%(owner)s)
    """, {'id': id, 'comment': comment, 'time': time,'owner':owner})


@connection.connection_handler
def get_comment_for_Q(cursor, id):
    cursor.execute("""
        SELECT id, message, submission_time FROM comment
        WHERE question_id=%(id)s;
    """, {'id': id})
    comments = cursor.fetchall()
    return comments


@connection.connection_handler
def add_comment_to_A(cursor, id, comment, time,owner):
    cursor.execute("""
        INSERT INTO comment (question_id, answer_id, message, submission_time, edited_count,owner)
        VALUES (NULL, %(id)s, %(comment)s,TIMESTAMP %(time)s, NULL,%(owner)s)
    """, {'id': id, 'comment': comment, 'time': time,'owner':owner})


@connection.connection_handler
def get_comment_for_A(cursor, id):
    cursor.execute("""
        SELECT id, message, submission_time FROM comment
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
def delete_comment(cursor, id,owner):
    cursor.execute("""
    DELETE FROM comment
    WHERE id=%(id)s and owner=%(owner)s
    """, {'id': id,'owner':owner})

@connection.connection_handler
def get_comment_for_edit(cursor, id):
    cursor.execute("""
        SELECT id, message FROM comment
        WHERE id=%(id)s;
    """, {'id': id})
    comment = cursor.fetchall()
    return comment

@connection.connection_handler
def update_comment(cursor, comment, submission_time, id,owner):
    cursor.execute("""
            UPDATE comment
            SET message=%(comment)s, submission_time=%(submission_time)s, edited_count=edited_count + 1,owner=%(owner)s
            WHERE id=%(id)s
    """, {'id': id, 'comment': comment, 'submission_time': submission_time,'owner':owner})

@connection.connection_handler
def delete_existing_tag(cursor,question,tag):
    cursor.execute("""
                    DELETE FROM question_tag
                    WHERE question_id = %(question)s and tag_id = %(tag)s 
    """, {'question':question, 'tag':tag})

@connection.connection_handler
def get_tag_for_question(cursor,question):
    cursor.execute("""
                              SELECT name,id FROM question_tag,tag
                              WHERE question_id = %(question)s  and id = tag_id;
                             """,{'question':question}
                   )
    names = cursor.fetchall()
    return names

@connection.connection_handler
def create_tag(cursor,new_tags):
    cursor.execute("""
                   INSERT INTO tag (name)
                   VALUES (%(new_tags)s);
                   """,
                       {'new_tags':new_tags})

@connection.connection_handler
def get_question_id_by_answer_id(cursor, id):
    cursor.execute("""
    SELECT * FROM answer
    WHERE id=%(id)s;
    """, {'id': id})
    q_id = cursor.fetchall()
    return q_id

def hash_password(text):
    # By using bcrypt, the salt is saved into the hash itself
    hashed_bytes = bcrypt.hashpw(text.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')

def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)

@connection.connection_handler
def SQL_password_username(cursor,psw,user,time):
    cursor.execute("""
                    INSERT INTO users (username, password, creation_date)
                    VALUES (%(user)s,%(psw)s,%(time)s);
    """, {'user':user, 'psw':psw, 'time':time})

@connection.connection_handler
def get_answer_id_by_question_id(cursor, id):     #SZAR
    cursor.execute("""
    SELECT * FROM answer
    WHERE question_id=%(id)s;
    """, {'id': id})
    row = cursor.fetchall()
    return row

@connection.connection_handler
def get_all_users(cursor):
    cursor.execute("""
    SELECT * from users
    ORDER BY id;
    """)
    users = cursor.fetchall()
    return users

@connection.connection_handler
def get_one_user(cursor,username):
    cursor.execute("""
    SELECT * from users
    WHERE username=%(username)s;
    """, {'username': username})
    user_row = cursor.fetchall()
    return user_row

@connection.connection_handler
def write_cookie_value_to_user(cursor, username, cookie_value):
    cursor.execute("""
    UPDATE users
    SET cookie_value=%(cookie_value)s
    WHERE username=%(username)s
    """, {'username': username, 'cookie_value': cookie_value})

@connection.connection_handler
def get_user_question(cursor, username):
    cursor.execute("""
    SELECT * FROM question
    WHERE owner=%(username)s
    """, {'username': username})
    rows = cursor.fetchall()
    return rows

@connection.connection_handler
def get_user_answer(cursor, username):
    cursor.execute("""
    SELECT * FROM answer
    WHERE owner=%(username)s
    """, {'username': username})
    rows = cursor.fetchall()
    return rows

@connection.connection_handler
def get_user_comment(cursor, username):
    cursor.execute("""
    SELECT * FROM comment
    WHERE owner=%(username)s
    """, {'username': username})
    rows = cursor.fetchall()
    return rows

def verify_password(text, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(text.encode('utf-8'), hashed_bytes_password)

@connection.connection_handler
def get_owner_by_id(cursor,id):
    cursor.execute("""
                    SELECT owner FROM question
                    WHERE  id = %(id)s;  
    """,{'id':id})

    names = cursor.fetchall()
    return names

@connection.connection_handler
def get_owner_answer(cursor,id):
    cursor.execute("""
                        SELECT owner FROM answer
                        WHERE  id = %(id)s;  
        """, {'id': id})

    names = cursor.fetchall()
    return names

@connection.connection_handler
def get_comment_owner(cursor,id):
    cursor.execute("""
                        SELECT owner FROM comment
                        WHERE  id = %(id)s;  
        """, {'id': id})

    names = cursor.fetchall()
    return names

@connection.connection_handler
def get_user_info(cursor, username):
    cursor.execute("""
    SELECT * FROM users
    WHERE username=%(username)s;
    """, {'username': username})
    row = cursor.fetchall()
    return row

@connection.connection_handler
def question_upvote_reputation(cursor, username):
    cursor.execute("""
    UPDATE users
    SET reputation = reputation + 5
    WHERE username=%(username)s;
    """, {'username': username})

@connection.connection_handler
def question_downvote_reputation(cursor, username):
    cursor.execute("""
    UPDATE users
    SET reputation = reputation - 2
    WHERE username=%(username)s;
    """, {'username': username})

@connection.connection_handler
def answer_upvote_reputation(cursor, username):
    cursor.execute("""
    UPDATE users
    SET reputation = reputation + 10
    WHERE username=%(username)s;
    """, {'username': username})

@connection.connection_handler
def answer_downvote_reputation(cursor, username):
    cursor.execute("""
    UPDATE users
    SET reputation = reputation - 2
    WHERE username=%(username)s;
    """, {'username': username})

@connection.connection_handler
def all_tags_used(cursor):
    cursor.execute("""
                    SELECT tag.name ,COUNT(tag_id) AS Appearance FROM question_tag
                    LEFT JOIN tag ON question_tag.tag_id = tag.id
                    GROUP BY tag.name
    
    """)

    names = cursor.fetchall()
    return names