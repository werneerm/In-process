from flask import Flask, render_template, request, redirect, url_for

import data_handler

DATA_HEADER = ['id', 'submisson_time', 'view_number', 'vote_number', 'title', 'message', 'image']

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
        question = data_handler.get_all_questions()
        return render_template('/questions.html', question = question)
if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
