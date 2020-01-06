from flask import Flask, render_template, request, redirect, url_for

import data_handler

app = Flask(__name__)

@app.route('/')
@app.route('/list')
def route_list():
    question = data_handler.get_all_question()

    return render_template('list.html', question=question)


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
