from flask import Flask, render_template, url_for, request, flash, redirect, abort
from flask_sqlalchemy import SQLAlchemy as Sql
from sqlalchemy import create_engine
from werkzeug import secure_filename
from forms import WordForm, PuzzleForm
import sys
import os

app = Flask(__name__)
UPLOAD_DIR = 'static/uploads'
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
HOST = os.environ['HOST']
PORT = os.environ['PORT']
DEBUG = os.environ['DEBUG']

db = Sql(app)

# from models import Word, Puzzle
from dictionary_builder import add_single_word, add_from_file
from puzzle_builder import build_puzzle, build_game

db.create_all()


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/add_word', methods=['get', 'post'])
def add_word():
    print(request.method, file=sys.stderr)
    if request.method == 'POST' and request.form:
        print(request.form, file=sys.stderr)
        word = request.form.get('word')
        category = request.form.get('category')
        message = add_single_word(word, category)
        flash(message)
        form = WordForm()
        return render_template('add_word.html', title='Add Word', form=form)
    else:
        form = WordForm()
        return render_template('add_word.html', title='Add Word', form=form)


@app.route('/uploader', methods=['post'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        if not f:
            flash('Please attach a csv file with the words')
            form = WordForm()
            return render_template('add_word.html', form=form, title='Add Word')
        category = request.form.get('category')
        print(category, file=sys.stderr)
        filename = '/'.join([UPLOAD_DIR, secure_filename(f.filename)])
        f.save(filename)
        message = add_from_file(filename, category)
        flash(message)
        return render_template('home.html')


@app.route('/create_puzzle/<puzzle_id>', methods=['get'])
@app.route('/create_puzzle', methods=['get', 'post'])
def create_puzzle(puzzle_id=None):
    if request.method == 'POST' and request.form:
        question = request.form.get('question')
        answer = request.form.get('answer')
        difficulty = request.form.get('difficulty')
        message, puzzle_id = build_puzzle(question, answer, difficulty)
        flash(message)
        return redirect(url_for('play_game', game_id=puzzle_id))
    else:
        form = PuzzleForm()
    return render_template('create_puzzle.html', title='Create Puzzle', form=form)


@app.route('/play_game/<game_id>', methods=['get'])
def play_game(game_id):
    message, game = build_game(game_id)
    if not message == 'success':
        flash(message)
        return render_template('404.html', title='404', missing_object='Puzzle'), 404
    else:
        return render_template('play_game.html', game=game, title='Play')


@app.errorhandler(404)
def page_not_found(missing_object):
    return render_template('404.html', title='404', missing_object='Page'), 404


if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host='0.0.0.0', port=5000, debug=True)
