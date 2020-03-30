from wtforms import SelectField, SelectMultipleField, SubmitField, IntegerField, StringField
# from models import Word, Puzzle
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm


class WordForm(FlaskForm):
    word = StringField('Word', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    submit = SubmitField('Add')


class PuzzleForm(FlaskForm):
    question = StringField('Question', validators=[DataRequired()])
    answer = StringField('Answer', validators=[DataRequired()])
    difficulty = SelectField('Difficulty', choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])
    submit = SubmitField('Build')


class KeywordForm(FlaskForm):
    word = StringField('KeyWord', validators=[DataRequired()])
    keys = StringField('KeyLetters', validators=[DataRequired()])


