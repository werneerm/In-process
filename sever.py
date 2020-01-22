from flask import Flask, render_template, request, redirect, url_for
import data_handler
import time
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def only_5_question():
    question = data_handler.get_top_question_sql()
    return render_template('list.html', question=question)

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
        comment_for_Q = data_handler.get_comment_for_Q(id)
        comment_for_A = data_handler.get_comment_for_A(id)  #SZAR
        return render_template('/questions.html', question=question, id=id, answer=answer, comment_Q=comment_for_Q, comment_A=comment_for_A)


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


@app.route('/questions/<int:id>/delete-question', methods=['GET', 'POST'])
def delete_question(id=None):
    if request.method == 'POST':
        option = request.form['pick']
        if option == 'yes':
            data_handler.delete_SQL_question_and_its_answer(id)
            data_handler.delete_SQL_comment_with_question(id)
            data_handler.delete_SQL_question(id)
            return redirect(url_for('route_list'))
        elif option == 'no':
            return redirect(url_for('questions_site', id=id))
    if request.method == 'GET':
        return render_template('question-delete.html', id=id)


#@app.route('/questions/<int:id>/a', methods=['GET', 'POST'])
@app.route('/questions/<int:id>/delete_answer', methods=['GET', 'POST'])
def delete_answer(id=None):
    data_handler.delete_SQL_answer(id)
    return redirect(url_for('questions_site', id=id))

@app.route('/list/<sort>', methods=['GET'])
def sorting(sort):
    request.path == '/list/<sort>'
    question = data_handler.sorting_sql(sort)
    return render_template('list.html', question=question)


@app.route('/list/<dsort>/desc', methods=['GET', 'POST'])
def sorting_desc(dsort):
    request.path == '/list/<sort>/desc'
    question = data_handler.sorting_sql_desc(dsort)
    return render_template('list.html', question=question)



@app.route('/questions/<int:id>/add-comment-to-Q', methods=['GET', 'POST'])
def add_comment_to_Q(id):
    if request.method == 'GET':
        return render_template('new-comment.html', id=id)
    if request.method == 'POST':
        comment = request.form['message']
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data_handler.add_comment_to_Q(id, comment, time)
        return redirect(url_for('questions_site', id=id))

@app.route('/answer/<int:id>/add-comment-to-A', methods=['GET', 'POST'])
def add_comment_to_A(id):
    if request.method == 'GET':
        return render_template('new-comment-for-answer.html', id=id)
    if request.method == 'POST':
        comment = request.form['message']
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data_handler.add_comment_to_A(id, comment, time)
        question_id = data_handler.ID_from_answer(id)
        ID_ANS = 0
        for line in question_id:                                #FOSSZARHUGY
            ID_ANS = line
        return redirect(url_for('route_list'))

@app.route('/search')
def search():
    searched_word = request.args.get('search')
    q_tilte = data_handler.search_title(searched_word)
    q_message = data_handler.search_message(searched_word)
    a_message = data_handler.answer_search_message(searched_word)
    search1 = q_tilte+q_message+a_message
    return render_template('search.html', search=search1)


@app.route('/questions/<int:id>/vote_up')
def ques_upvote(id=None):
    data_handler.upvote_questions_SQL(id)
    return redirect(url_for('route_list'))

@app.route('/questions/<int:id>/vote_down')
def ques_downvote(id=None):
    data_handler.downvote_questions_SQL(id)
    return redirect(url_for('route_list'))

@app.route('/answers/<int:id>/vote_up')
def answer_upvote(id=None):
    data_handler.upvote_answers_SQL(id)
    return redirect(url_for('route_list'))

@app.route('/answers/<int:id>/vote_down')
def answer_downvote(id=None):
    data_handler.downvote_answers_SQL(id)
    return redirect(url_for('route_list'))

@app.route('/answers/<int:id>/edit-answer', methods=['GET', 'POST'])
def edit_answer(id=None):
    if request.method == 'GET':
        answer = data_handler.get_answer_for_update(id)
        return render_template('edit-answer.html', answer=answer)
    if request.method == 'POST':
        new_message = request.form['message']
        new_image = request.form['image']
        data_handler.answer_update_SQL(new_message, new_image, id)
        return redirect(url_for('route_list'))

@app.route('/comment/<int:id>/delete-comment', methods=['GET', 'POST'])
@app.route('/comment/<int:id>/edit-comment', methods=['GET', 'POST'])
def comment(id=None):
    if request.path == f'/comment/{id}/delete-comment':
        data_handler.delete_comment(id)
        return redirect(url_for('route_list'))
    if request.path == f'/comment/{id}/edit-comment':
        if request.method == 'GET':
            comment = data_handler.get_comment_for_edit(id)
            return render_template('edit-comment.html',comment=comment)
        if request.method == 'POST':
            new_comment = request.form['message']
            new_sub_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            data_handler.update_comment(new_comment, new_sub_time, id)
            return redirect(url_for('route_list'))

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
