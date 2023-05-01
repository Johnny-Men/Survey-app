from flask import Flask,request,render_template,redirect,flash,session
from flask_debugtoolbar import DebugToolbarExtension
from random import randint,choice,sample
from surveys import *

app = Flask(__name__)

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = 'glob23'
debug = DebugToolbarExtension(app)

counter = 0

@app.route('/')
def render_home_page():
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    return render_template('base.html', title=title, instructions=instructions)

@app.route('/session-list', methods=['POST'])
def create_session_list():
    session['responses'] = []
    return redirect('/question/0')

@app.route('/question/<int:num>')
def render_question(num):
    responses = session['responses']
    if num != len(responses):
        flash('Invalid question', 'error')
    else:
        question = satisfaction_survey.questions[num].question
        choices = satisfaction_survey.questions[num].choices
        start = 'start'
        return render_template('question.html', question=question, choices=choices)
    return redirect(f'/question/{len(responses)}')

@app.route('/answer', methods=['POST'])
def append_answer_next():
    responses = session['responses']
    responses.append(request.form['answer'])
    session['responses'] = responses
    if len(responses) == len(satisfaction_survey.questions):
        return redirect('/thanks')
    else:
        return redirect(f'/question/{len(responses)}')

@app.route('/thanks')
def say_thanks():
    return render_template('thanks.html')

    
    
