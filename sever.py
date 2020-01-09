from flask import Flask, render_template, request, redirect, url_for

import data_handler
import time

DATA_HEADER = ['id', 'submisson_time', 'view_number', 'vote_number', 'title', 'message', 'image']
DATA_FILE_PATH_QUESTION = "./sample_data/question.csv"
DATA_FILE_PATH_ANSWER = "./sample_data/answer.csv"


app = Flask(__name__)
@app.route('/')
@app.route('/list')
def route_list():
    question = data_handler.get_all_questions()

    return render_template('list.html', question= question,)


@app.route('/questions/<int:id>', methods=['GET','POST'])
def questions_site(id = None):
    if request.method == 'POST':
        new_question = request.form.to_dict()
        data_handler.add_question(new_question)

        return redirect("/")

    if id is not None :
        answer = data_handler.index_finder(id)
        return render_template('/questions.html', answer=answer,id=id)


@app.route('/questions/<int:id>', methods=['GET', 'POST'])
@app.route('/questions/<int:id>/answer-question', methods=['GET', 'POST'])
def add_answer(id=None):
    if request.method == 'GET':
        return render_template('/new_answer.html',id=id)
    if request.method == 'POST':
        message = request.form['message']
        image = request.form['image']
        table = data_handler.get_all_answer()
        new_answer_list = []
        new_answer_list.append(str(int(table[-1][0]) + 1))
        new_answer_list.append(str(time.time()))
        new_answer_list.append('0')
        new_answer_list.append(str(id))
        new_answer_list.append(message)
        new_answer_list.append(image)
        table.append(new_answer_list)
        data_handler.write_user_story(DATA_FILE_PATH_ANSWER, table)
        answer = data_handler.index_finder(id)
        return redirect(f'/questions/{id}')

@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    if request.method == 'POST':
        title = request.form['title']
        message = request.form['message']
        table = data_handler.get_all_questions()
        new_quest_list = []
        new_quest_list.append(data_handler.id_generator(table))
        new_quest_list.append(str(time.time()))
        new_quest_list.append('0')
        new_quest_list.append('0')
        new_quest_list.append(title)
        new_quest_list.append(message)
        table.append(new_quest_list)
        data_handler.write_user_story(DATA_FILE_PATH_QUESTION, table)
        return redirect('/')
    return render_template('add-question.html')

@app.route('/answers/<int:id>/vote_up')
def ans_upvote(id = None):
     table = data_handler.get_all_answer()
     if id is not None:
        question_id = ""
        vote_num = ""
        line_num = None
        for idx , line in enumerate(table):
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
