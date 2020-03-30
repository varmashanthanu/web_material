from app import db
from models import Word
import pandas as pd
import sys


def add_single_word(word, category):
    if Word.query.filter_by(name=word).first():
        return 'Word already exists'
    letters = list(word)
    letters.sort()
    letters = ''.join(letters)
    anagrams = Word.query.filter_by(letters=letters).all()
    if anagrams:
        for anagram in anagrams:
            db.session.delete(anagram)
        db.session.commit()
        return 'An anagram for this word exists'
    length = len(word)
    new_word = Word(name=word, length=length, category=category, letters=letters)
    db.session.add(new_word)
    db.session.commit()
    return '"'+word+'" has been added.'


def get_letters(row):
    word = row['Word'].upper()
    letters = list(word)
    letters.sort()
    letters = ''.join(letters)
    return letters


def add_from_file(filename, category):
    df = pd.read_csv(filename)
    df = df[['Word']]
    print(df.head(), file=sys.stderr)
    df['Letters'] = df.apply(get_letters, axis=1)
    df.drop_duplicates(subset=['Letters'])
    for i, row in df.iterrows():
        letters = row['Letters']
        if not Word.query.filter_by(letters=letters).first():
            word = row['Word'].upper()
            length = len(word)
            new_word = Word(name=word, letters=letters, category=category, length=length)
            db.session.add(new_word)
        if i % 5000 == 0:
            db.session.commit()
    db.session.commit()
    return 'Added all words'
