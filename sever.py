from flask import Flask, render_template, request, redirect, url_for
import data_handler
import time
from datetime import datetime

DATA_HEADER = ['id', 'submisson_time', 'view_number', 'vote_number', 'title', 'message', 'image']
DATA_FILE_PATH_QUESTION = "./sample_data/question.csv"
DATA_FILE_PATH_ANSWER = "./sample_data/answer.csv"

app = Flask(__name__)


@app.route('/')
@app.route('/list')
def route_list():
    question = data_handler.get_all_question_sql()
    return render_template('list.html', question=question)


@app.route('/questions/<int:id>', methods=['GET', 'POST'])
def questions_site(id=None):
    if request.method == 'POST':
        new_question = request.form.to_dict()
        data_handler.add_question(new_question)

        return redirect("/")

    if id is not None:
        #the_question, the_message, the_image = data_handler.question_finder(id)
        question = data_handler.get_question_SQL(id)
        answer = data_handler.get_answer_for_question_SQL(id)
        return render_template('/questions.html', question=question, id=id, answer=answer)


@app.route('/questions/<int:id>', methods=['GET', 'POST'])
@app.route('/questions/<int:id>/answer-question', methods=['GET', 'POST'])
def add_answer(id=None):
    if request.method == 'GET':
        return render_template('/new_answer.html', id=id)
    if request.method == 'POST':
        message = request.form['message']
        image = request.form['image']
        table = data_handler.get_all_answer()
        new_answer_list = []
        new_answer_list.append(str(int(table[-1][0]) + 1))
        new_answer_list.append(str(int(time.time())))
        new_answer_list.append('0')
        new_answer_list.append(str(id))
        new_answer_list.append(message)
        new_answer_list.append(image)
        #table.append(new_answer_list)
        #data_handler.write_user_story(DATA_FILE_PATH_ANSWER, table)
        # answer = data_handler.index_finder(id)
        # return render_template('/questions.html',answer=answer,id=id, question=the_question, message=the_message)
        return redirect(url_for('questions_site', id=id))


@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    if request.method == 'POST':
        title = request.form['title']
        message = request.form['message']
        image = request.form['image']
        table = data_handler.get_all_questions()
        vote_number = 0
        view_number = 0
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # new_quest_list = ""
        # new_quest_list.join(data_handler.id_generator(table)+ ';')
        # new_quest_list.join(time.time() + ";")
        # new_quest_list.join('0'+ ";")
        # new_quest_list.join('0' + ";")
        # new_quest_list.join(title + ";")
        # new_quest_list.join(message + ";")
        # new_quest_list.join(image + ";")
        data_handler.add_SQL_question(time, view_number, vote_number, title, message, image)
        # data_handler.add_SQL_question(new_quest_list)
        return redirect(url_for('questions_site', id=table[-1][0]))
    return render_template('add-question.html')


@app.route('/questions/<int:id>', methods=['GET', 'POST'])
@app.route('/questions/<int:id>/edit-question', methods=['GET', 'POST'])
def edit_question(id=None):
    if request.method == 'GET':
        question, message, image = data_handler.question_finder(id)
        return render_template('edit-question.html', id=id, question=question, message=message, image=image)
    elif request.method == 'POST':
        table = data_handler.get_all_questions()
        changed_title = request.form['title']
        changed_message = request.form['message']
        changed_image = request.form['image']
        data_handler.question_change(changed_title, changed_message, changed_image, table, id)
        return redirect(url_for('questions_site', id=id))


@app.route('/questions/<int:id>/d', methods=['GET', 'POST'])
@app.route('/questions/<int:id>/delete-question', methods=['GET', 'POST'])
def delete_question(id=None):
    if request.method == 'POST':
        option = request.form['pick']
        if option == 'yes':
            table = data_handler.get_all_questions()

            answers = data_handler.get_all_answer()
            # for i in answers:
            #     if id == i[3]:

            data_handler.delete_question(id, table, answers)
            return redirect(url_for('route_list'))
        elif option == 'no':
            return redirect(url_for('questions_site', id=id))
    if request.method == 'GET':
        return render_template('question-delete.html', id=id)


@app.route('/questions/<int:id>/a', methods=['GET', 'POST'])
@app.route('/questions/<int:id>/delete_answer', methods=['GET', 'POST'])
def delete_answer(id=None):
    if request.method == 'POST':
        option = request.form['choose']
        table = data_handler.get_all_answer()
        if option == 'yes':
            question_id = data_handler.delete_answer(id, table)
            return redirect(url_for('questions_site', id=question_id))
        elif option == 'no':
            question_id = ""
            for line in table:
                if str(line[0]) == str(id):
                    question_id = line[3]
            return redirect(url_for('questions_site', id=question_id))
    if request.method == 'GET':
        return render_template('delete_answer.html', id=id)


@app.route('/list/ID', methods=['GET'])
@app.route('/list/SubmissionTime', methods=['GET'])
@app.route('/list/ViewNumber', methods=['GET'])
@app.route('/list/VoteNumber', methods=['GET'])
@app.route('/list/Title', methods=['GET'])
@app.route('/list/Message', methods=['GET'])
def sorting():
    if request.path == '/list/ID':
        question = data_handler.sorting_things('id')
        return render_template('list.html', question=question)
    elif request.path == '/list/SubmissionTime':
        question = data_handler.sorting_things('submisson_time')
        return render_template('list.html', question=question)
    elif request.path == '/list/ViewNumber':
        question = data_handler.sorting_things('view_number')
        return render_template('list.html', question=question)
    elif request.path == '/list/VoteNumber':
        question = data_handler.sorting_things('vote_number')
        return render_template('list.html', question=question)
    elif request.path == '/list/Title':
        question = data_handler.sorting_things('title')
        return render_template('list.html', question=question)
    elif request.path == '/list/Message':
        question = data_handler.sorting_things('message')
        return render_template('list.html', question=question)


@app.route('/answers/<int:id>/vote_up')
def ans_upvote(id=None):
    table = data_handler.get_all_answer()
    if id is not None:
        question_id = ""
        vote_num = ""
        line_num = None
        for idx, line in enumerate(table):
            if str(id) == line[0]:
                question_id = line[3]
                vote_num = line[2]
                line_num = idx

        int_vote_num = int(vote_num)
        int_vote_num += 1
        str_vote_num = str(int_vote_num)
        table[line_num][2] = str_vote_num
        data_handler.write_user_story(DATA_FILE_PATH_ANSWER, table)
        return redirect(f'/questions/{question_id}')


@app.route('/answers/<int:id>/vote_down')
def ans_downvote(id=None):
    answers = data_handler.get_all_answer()
    if id is not None:
        question_id = ""
        vote_num = ""
        line_num = None
        for idx, line in enumerate(answers):
            if str(id) == line[0]:
                question_id = line[3]
                vote_num = line[2]
                line_num = idx

        int_vote_num = int(vote_num)
        int_vote_num = int_vote_num - 1
        str_vote_num = str(int_vote_num)
        answers[line_num][2] = str_vote_num
        data_handler.write_user_story(DATA_FILE_PATH_ANSWER, answers)
        return redirect(f'/questions/{question_id}')


@app.route('/questions/<int:id>/vote_up')
def ques_upvote(id=None):
    table = data_handler.get_all_questions()
    if id is not None:
        vote_num = ""
        line_num = None
        for idx, line in enumerate(table):
            if str(id) == line[0]:
                vote_num = line[3]
                line_num = idx
        int_vote_num = int(vote_num)
        int_vote_num += 1
        str_vote_num = str(int_vote_num)
        table[line_num][3] = str_vote_num
        data_handler.write_user_story(DATA_FILE_PATH_QUESTION, table)
        return redirect('/list')
    return redirect(url_for('questions_site', id=id))


@app.route('/questions/<int:id>/vote_down')
def ques_down(id=None):
    table = data_handler.get_all_questions()
    if id is not None:
        vote_num = ""
        line_num = None
        for idx, line in enumerate(table):
            if str(id) == line[0]:
                vote_num = line[3]
                line_num = idx
        int_vote_num = int(vote_num)
        int_vote_num = int_vote_num - 1
        str_vote_num = str(int_vote_num)
        table[line_num][3] = str_vote_num
        data_handler.write_user_story(DATA_FILE_PATH_QUESTION, table)
        return redirect('/list')


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
