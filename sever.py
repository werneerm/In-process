from flask import Flask, render_template, request, redirect, url_for,session
import data_handler
import time
from datetime import datetime
import bcrypt

app = Flask(__name__)
app.secret_key = '6w:`tFm%mBLY}ty*QcRRpD+,Jga@Fy\XFxjhga'


# @app.route('/')
# def only_5_question():
#     question = data_handler.get_top_question_sql()
#     return render_template('list.html', question=question)
@app.route('/')
@app.route('/list')
def route_list():
    if session.get('username'):
        question = data_handler.get_all_question_sql()
        tag = data_handler.question_tag()
        choose_the_one = data_handler.get_all_tag()
        user = data_handler.get_one_user(session['username'])
        print(user)
        return render_template('list.html', question=question, tag=tag, match=choose_the_one, user=user)
    else:
        question = data_handler.get_all_question_sql()
        tag = data_handler.question_tag()
        choose_the_one = data_handler.get_all_tag()
        return render_template('list.html', question=question, tag=tag, match=choose_the_one,)
    # question = data_handler.get_all_question_sql()
    # tag = data_handler.question_tag()
    # choose_the_one = data_handler.get_all_tag()
    # return render_template('list.html', question=question, tag=tag, match=choose_the_one)


@app.route('/questions/<int:id>', methods=['GET', 'POST'])
def questions_site(id=None):
    #if id is not None:
    question = data_handler.get_question_SQL(id)
    answer = data_handler.get_answer_for_question_SQL(id)
    comment_for_Q = data_handler.get_comment_for_Q(id)
    tag = data_handler.question_tag()
    choose_the_one = data_handler.get_all_tag()
    comment_for_A = data_handler.get_comment_for_A(id)  #SZAR
    return render_template('/questions.html', question=question, id=id, tag=tag, match=choose_the_one, answer=answer, comment_Q=comment_for_Q, comment_A=comment_for_A)


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
        owner = session['username']
        data_handler.add_answer_SQL(time, vote_num, question_id, message, image, owner)
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
        owner = session['username']
        data_handler.add_SQL_question(time, view_number, vote_number, title, message, image, owner)
        return redirect(url_for('route_list'))
    return render_template('add-question.html')


#@app.route('/questions/<int:id>', methods=['GET', 'POST'])
@app.route('/questions/<int:id>/edit-question', methods=['GET', 'POST'])
def edit_question(id=None):
    if request.method == 'GET':
        row = data_handler.question_finder_SQL(id)
        return render_template('edit-question.html', id=id, row=row)
    elif request.method == 'POST':
        row = data_handler.question_finder_SQL(id)
        user = session['username']
        user_row = data_handler.get_owner_by_id(id)
        user_infos = []
        for i in user_row:
            user_infos.append(i)
        if user_infos[0]['owner'] == user:
            changed_title = request.form['title']
            changed_message = request.form['message']
            changed_image = request.form['image']
            data_handler.question_update_SQL(changed_title, changed_message, changed_image, id,user)
            return redirect(url_for('questions_site', id=id))
    return render_template('edit-question.html', id=id, row=row)

@app.route('/questions/<int:id>/d', methods=['GET', 'POST'])
@app.route('/questions/<int:id>/delete-question', methods=['GET', 'POST'])
def delete_question(id=None):
    try:
        if request.method == 'POST':
            user = session['username']
            user_row = data_handler.get_owner_by_id(id)
            user_infos = []
            for i in user_row:
                user_infos.append(i)
            if user_infos[0]['owner'] == user:
                option = request.form['pick']
                if option == 'yes':
                    data_handler.delete_SQL_question(id,user)
                    return redirect(url_for('route_list'))
                elif option == 'no':
                    return redirect(url_for('questions_site', id=id))
            else:
                fail = "failed"
                return redirect(url_for('questions_site', id=id, fail=fail))
    except TypeError:
        fail = "failed"
        return redirect(url_for('questions_site', id=id,fail=fail))
    if request.method == 'GET':
        return render_template('question-delete.html', id=id)


@app.route('/questions/<int:id>/delete_answer')
def delete_answer(id=None):
    user = session['username']
    print(user)
    data_handler.delete_SQL_answer(id,user)
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
        user = session['username']
        comment = request.form['message']
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data_handler.add_comment_to_Q(id, comment, time,user)
        return redirect(url_for('questions_site', id=id))

@app.route('/answer/<int:id>/add-comment-to-A', methods=['GET', 'POST'])
def add_comment_to_A(id):
    if request.method == 'GET':
        return render_template('new-comment-for-answer.html', id=id)
    if request.method == 'POST':
        user= session['username']
        comment = request.form['message']
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data_handler.add_comment_to_A(id, comment, time,user)
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
    search1 = q_tilte + q_message + a_message
    return render_template('search.html', search=search1)


@app.route('/question/<int:id>/new-tag')
def tags(id=None):
    tag = data_handler.get_all_tag()
    return render_template('tag.html', tag=tag, id=id)



@app.route('/question/<int:id>/new-tag/<existing_tag>')
def add_pls(id=None, existing_tag=None):
    data_handler.add_existing_tag(existing_tag, id)
    return redirect(url_for('questions_site', id=id))


@app.route('/questions/<int:id>/vote_up')
def ques_upvote(id=None):
    data_handler.upvote_questions_SQL(id)
    question_row = data_handler.get_question_SQL(id)
    data = []
    for i in question_row:
        data.append(i)
    username = data[0]['owner']
    data_handler.question_upvote_reputation(username)
    return redirect(url_for('route_list'))


@app.route('/questions/<int:id>/vote_down')
def ques_downvote(id=None):
    data_handler.downvote_questions_SQL(id)
    question_row = data_handler.get_question_SQL(id)
    data = []
    for i in question_row:
        data.append(i)
    username = data[0]['owner']
    data_handler.question_downvote_reputation(username)
    return redirect(url_for('route_list'))


@app.route('/answers/<int:id>/vote_up')
def answer_upvote(id=None):
    data_handler.upvote_answers_SQL(id)
    realdictrow = data_handler.get_question_id_by_answer_id(id)
    list_for_realdictrow = []
    for i in realdictrow:
        list_for_realdictrow.append(i)
    question_id = list_for_realdictrow[0]['question_id']
    username = list_for_realdictrow[0]['owner']
    data_handler.answer_upvote_reputation(username)
    return redirect(url_for('questions_site', id=question_id))


@app.route('/answers/<int:id>/vote_down')
def answer_downvote(id=None):
    data_handler.downvote_answers_SQL(id)
    realdictrow = data_handler.get_question_id_by_answer_id(id)
    list_for_realdictrow = []
    for i in realdictrow:
        list_for_realdictrow.append(i)
    question_id = list_for_realdictrow[0]['question_id']
    username = list_for_realdictrow[0]['owner']
    data_handler.answer_downvote_reputation(username)
    return redirect(url_for('questions_site', id=question_id))


@app.route('/answers/<int:id>/edit-answer', methods=['GET', 'POST'])
def edit_answer(id=None):
    if request.method == 'GET':
        answer = data_handler.get_answer_for_update(id)
        return render_template('edit-answer.html', answer=answer)
    if request.method == 'POST':
        user = session['username']
        user_row = data_handler.get_owner_answer(id)
        user_infos = []
        for i in user_row:
            user_infos.append(i)
        if user_infos[0]['owner'] == user:
            new_message = request.form['message']
            new_image = request.form['image']
            data_handler.answer_update_SQL(new_message, new_image, id,user)
            return redirect(url_for('route_list'))
    return render_template('edit-answer.html', answer=answer)

@app.route('/comment/<int:id>/delete-comment', methods=['GET', 'POST'])
@app.route('/comment/<int:id>/edit-comment', methods=['GET', 'POST'])
def comment(id=None):
    if request.path == f'/comment/{id}/delete-comment':
        user = session['username']
        data_handler.delete_comment(id,user)
        return redirect(url_for('route_list'))
    if request.path == f'/comment/{id}/edit-comment':
        if request.method == 'GET':
            comment = data_handler.get_comment_for_edit(id)
            return render_template('edit-comment.html', comment=comment)
        if request.method == 'POST':
            user = session['username']
            user_row = data_handler.get_owner_by_id(id)
            user_infos = []
            for i in user_row:
                user_infos.append(i)
            if user_infos[0]['owner'] == user:
                new_comment = request.form['message']
                new_sub_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                data_handler.update_comment(new_comment, new_sub_time, id,user)
                return redirect(url_for('route_list'))
        return render_template('edit-comment.html', comment=comment)
@app.route('/error')
def sever_error():
    return render_template('error.html')


@app.route("/question/<int:id>/delete-tag")
def show_delete_tag(id=None):
    if id is not None:
        tags = data_handler.get_tag_for_question(id)
        #print(tags)
        return render_template('delete_tag.html',id=id,tags=tags)


@app.route('/question/<int:id>/delete-tag/<delete_tag>')
def delete_tag(id=None,delete_tag=None):
    data_handler.delete_existing_tag(id,delete_tag)
    return redirect(url_for('questions_site',id=id))

@app.route("/question/<int:id>/create-tag",methods=['GET','POST'])
def create_tag(id=None):
    if request.method == 'POST':
        new_tag=request.form['tag']
        data_handler.create_tag(new_tag)
        return redirect(url_for('questions_site',id=id))
    return render_template('tag.html',id=id)

@app.route("/question/<int:question_id>/answer/<int:answer_id>",methods=['GET','POST'])
def show_answer_comments(question_id=None, answer_id=None):
    question = data_handler.get_question_SQL(question_id)
    answer = data_handler.get_answer_for_question_SQL_with_ans_id(answer_id)
    comment = data_handler.get_comment_for_A(answer_id)
    return render_template('quest_ans_comment.html', question=question, answer=answer, comments=comment)

@app.route("/question/<int:question_id>/answer/<int:answer_id>/comments",methods=['GET','POST'])
def add_comment_to_answer(question_id=None, answer_id=None):
    question = data_handler.get_question_SQL(question_id)
    answer = data_handler.get_answer_for_question_SQL_with_ans_id(answer_id)
    if request.method == 'POST':
        user= session['username']
        comment = request.form['message']
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data_handler.add_comment_to_A(answer_id, comment, time,user)
        return redirect(url_for('questions_site', id=question_id))

    return render_template('new-comment-for-answer.html', quest=question_id, ans_id=answer_id)

@app.route("/question/<int:question_id>/delete_this/<int:comment_id>/<int:answer_id>", methods=['GET', 'POST'])
@app.route("/question/<int:question_id>/edit_this/<int:comment_id>/<int:answer_id>", methods=['GET', 'POST'])
def delete_only_comment(question_id, comment_id, answer_id):
    if request.path == f'/question/{question_id}/delete_this/{comment_id}/{answer_id}':
        user=session['username']
        data_handler.delete_comment(comment_id,user)
        return redirect(url_for('show_answer_comments', question_id=question_id, answer_id=answer_id))
    if request.path == f'/question/{question_id}/edit_this/{comment_id}/{answer_id}':
        if request.method == 'POST':
            user = session['username']
            new_comment = request.form['message']
            new_sub_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            data_handler.update_comment(new_comment, new_sub_time, comment_id,user)
            return redirect(url_for('show_answer_comments', question_id=question_id, answer_id=answer_id))
    question = data_handler.get_question_SQL(question_id)
    answer = data_handler.get_answer_for_question_SQL_with_ans_id(answer_id)
    comment = data_handler.get_comment_for_edit(comment_id)
    return render_template('edit-comment.html', comment=comment, question=question, answer=answer)

@app.route('/registration',methods=['GET','POST'])
@app.route('/registration-error',methods=['GET','POST'])
def regist():
    if request.method == 'POST':
        current_time= datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        username = request.form['username']
        password = request.form['psw']
        password2 = request.form['psw-repeat']
        hashed_psw = data_handler.hash_password(password)
        if password == password2:
            data_handler.SQL_password_username(hashed_psw,username,current_time)
            return redirect(url_for('route_list'))
        else:
            return render_template('registration-error.html')

    return render_template('registration.html')

@app.route('/all-user')
def see_all_user():
    users = data_handler.get_all_users()
    return render_template('all_user.html', users=users)

@app.route('/set-cookie')
def cookie_insertion():
    redirect_to_index = redirect('/')
    response = make_response(redirect_to_index)
    response.set_cookie('username', username='values')
    return response

# @app.before_request
# def require_login():
#     if 'username' not in session and request.endpoint != 'login':
#         return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        fail = "good so far"
        return render_template('login.html', fail=fail)
    if request.method == "POST":
        user_name = request.form["username"]
        password = request.form["psw"]
        user_row = data_handler.get_one_user(user_name)
        user_infos = []
        for i in user_row:
            user_infos.append(i)
        try:
            user_name_if_exist = user_infos[0]['username']
            user_pw_if_exist = user_infos[0]['password']
            if user_name == user_name_if_exist:
                if data_handler.verify_password(password, user_pw_if_exist) is True:
                    session['username'] = user_name
                    data_handler.write_cookie_value_to_user(user_name, session['username'])
                    return redirect('/')
                else:
                    fail = "failed"
                    return render_template('login.html', fail=fail)
            # else:
            #     fail = "failed"
            #     return render_tempalte('login.html', fail=fail)
        except IndexError:
            fail = "failed"
            return render_template('login.html', fail=fail)
        # if not user:
        #     # Again, throwing an error is not a user-friendly
        #     # way of handling this, but this is just an example
        #     raise ValueError("Invalid username or password supplied")

        # Note we don't *return* the response immediately
        # session['username'] =user_name
        # return redirect('/')

@app.route('/user/<int:id>', methods=['GET', 'POST'])
def user_site(id):
    actual_username = session['username']
    user_info = data_handler.get_user_info(actual_username)
    user_questions = data_handler.get_user_question(actual_username)
    user_answer = data_handler.get_user_answer(actual_username)
    user_comment = data_handler.get_user_answer(actual_username)

    return render_template('user_site.html', user_question=user_questions, user_answer=user_answer, user_comment=user_comment, user_info=user_info)


@app.route('/tag')
def tag_site():
    all_tags = data_handler.all_tags_used()
    return render_template('alltags.html',all_tags=all_tags)

@app.route('/logout')
def logout():
    if request.method == 'GET':
        session.clear()
        return redirect('/')
    return redirect('/')

@app.route('/answers/<int:id>/accepted-answer')
def accept_answer(id=None):
    user = session['username']
    question = data_handler.get_question_by_answer_mark_edition(id)
    owner=[]
    user_infos = []
    for i in question:
        user_infos.append(i)
    the_whole_question = data_handler.get_question_SQL(user_infos[0]['question_id'])
    for i in the_whole_question:
        owner.append(i)
    if user == owner[0]['owner']:
        question_id = int(user_infos[0]['question_id'])
        data_handler.accepted_answer(id,question_id)
        question = data_handler.get_question_SQL(question_id)
        answer = data_handler.get_answer_for_question_SQL(question_id)
        comment_for_Q = data_handler.get_comment_for_Q(question_id)
        tag = data_handler.question_tag()
        choose_the_one = data_handler.get_all_tag()
        comment_for_A = data_handler.get_comment_for_A(question_id)
        return render_template('/questions.html', question=question, id=question_id, tag=tag, match=choose_the_one, answer=answer,
                               comment_Q=comment_for_Q, comment_A=comment_for_A)
    return redirect('/')
if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
