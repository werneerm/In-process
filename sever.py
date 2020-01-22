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
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        vote_num = 0
        question_id = id
        data_handler.add_answer_SQL(time, vote_num, question_id, message, image)
        return redirect(url_for('questions_site', id=id))


@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    if request.method == 'POST':
        title = request.form['title']
        message = request.form['message']
        image = request.form['image']
        vote_number = 0
        view_number = 0
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data_handler.add_SQL_question(time, view_number, vote_number, title, message, image)
        return redirect(url_for('route_list'))
    return render_template('add-question.html')


@app.route('/questions/<int:id>', methods=['GET', 'POST'])
@app.route('/questions/<int:id>/edit-question', methods=['GET', 'POST'])
def edit_question(id=None):
    if request.method == 'GET':
        row = data_handler.question_finder_SQL(id)
        return render_template('edit-question.html', id=id, row=row)
    elif request.method == 'POST':
        changed_title = request.form['title']
        changed_message = request.form['message']
        changed_image = request.form['image']
        data_handler.question_update_SQL(changed_title, changed_message, changed_image, id)
        return redirect(url_for('questions_site', id=id))


@app.route('/questions/<int:id>/d', methods=['GET', 'POST'])
@app.route('/questions/<int:id>/delete-question', methods=['GET', 'POST'])
def delete_question(id=None):
    if request.method == 'POST':
        option = request.form['pick']
        if option == 'yes':
            data_handler.delete_SQL_question(id)
            data_handler.delete_SQL_answer(id)
            return redirect(url_for('route_list'))
        elif option == 'no':
            return redirect(url_for('questions_site', id=id))
    if request.method == 'GET':
        return render_template('question-delete.html', id=id)


@app.route('/questions/<int:id>/a', methods=['GET', 'POST'])
@app.route('/questions/<int:id>/delete_answer', methods=['GET', 'POST'])
def delete_answer(id=None):
    data_handler.delete_SQL_answer(id)
    return redirect(url_for('questions_site', id=id))

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
    data_handler.upvote_answers_SQL(id)
    return redirect(url_for('questions_site', id=id))


@app.route('/answers/<int:id>/vote_down')
def ans_downvote(id=None):
    data_handler.downvote_answers_SQL(id)
    return redirect(url_for('questions_site', id=id))

@app.route('/questions/<int:id>/vote_up')
def ques_upvote(id=None):
    data_handler.upvote_questions_SQL(id)
    return redirect(url_for('questions_site', id=id))

@app.route('/questions/<int:id>/vote_down')
def ques_down(id=None):
    data_handler.downvote_questions_SQL(id)
    return redirect('/list')

@app.route('/search')
def search():
    searched_word = request.args.get('search')
    q_tilte = data_handler.search_title(searched_word)
    q_message = data_handler.search_message(searched_word)
    a_message = data_handler.answer_search_message(searched_word)
    search1 = q_tilte+q_message+a_message
    return render_template('search.html', search=search1)
if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
