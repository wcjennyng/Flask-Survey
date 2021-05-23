from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret_name'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

standard = 'responses'

@app.route('/')
def home_page():
    """Home page"""
    return render_template('home.html', survey=survey)

@app.route('/start', methods=['POST'])
def start():
    """Begins survey"""
    session[standard] = []
    return redirect('/questions/0')

@app.route('/questions/<int:num>')
def question_pg(num):
    """Show question"""

    responses = session.get(standard)

    if (len(responses) == len(survey.questions)):
        return redirect('/completed')

    if (len(responses) != num):
        flash(f"Invalid question number! Please refresh the page and start again.")
        return redirect('/')

    question = survey.questions[num]
    return render_template('questions.html', num=num, question=question)

@app.route('/response', methods=['POST'])
def response():
    """Answer and redirect to next question"""
    choice = request.form['response']

    #add to session
    responses = session[standard]
    responses.append(choice)
    session[standard] = responses

    if (len(responses) == len(survey.questions)):
        return redirect('/completed')
    else:
        return redirect(f"/questions/{len(responses)}")

@app.route('/completed')
def completed():
    """End of survey"""
    return render_template('completed.html')