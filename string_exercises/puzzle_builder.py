from app import db
from models import Word, Puzzle
import pandas as pd
import sys
import re
from random import randint, shuffle
import random
from math import ceil, floor


def get_random_keys(all_keys, length):
    keys = []
    for i in range(length):
        k = random.choice(all_keys)
        keys.append(k)
        all_keys.remove(k)
    return keys, all_keys


def get_word_suggestion(keys, length):
    word_filter = [Word.length <= length]
    letters = list(set(keys))
    keys_dict = {k: keys.count(k) for k in letters}
    for k, v in keys_dict.items():
        if v > 1:
            l_query = '%'
            for i in range(v):
                l_query = l_query + k + '%'
            l_query = l_query + '%'
        else:
            l_query = '%' + k + '%'
        word_filter.append(Word.letters.like(l_query))
    full_query = db.session.query(Word).filter(*word_filter)
    possible_words = full_query.all()
    if not possible_words:
        return None
    possible_word = random.choice(possible_words)
    return possible_word


def build_puzzle(question, answer, difficulty):
    question = question.upper()
    answer = answer.upper()
    difficulty = int(difficulty)
    print('Cleaning up', file=sys.stderr)
    regex = re.compile('[^a-zA-Z]')
    answer_root = regex.sub('', answer).upper()
    answer_letter_count = len(answer_root)

    print('Preparing', file=sys.stderr)
    min_key_count = 1
    max_key_count = 3

    min_word_length = ceil(4 * (1 + difficulty * 5 / 10))
    max_word_length = min_word_length + ceil(2 * (1 + difficulty * 5 / 10))

    puzzle_words = {'Word': [], 'Keys': [], 'Length': []}
    keys_list = list(answer_root.upper())
    print('making wordlist', file=sys.stderr)
    while keys_list:
        print(len(keys_list), 'remaining:', keys_list)
        key_length = randint(min_key_count, min(len(keys_list), max_key_count))
        word_keys, keys_list = get_random_keys(keys_list, key_length)
        word_length = randint(min_word_length, max_word_length)
        print(word_keys, word_length, keys_list, file=sys.stderr)
        possible_word = get_word_suggestion(word_keys, word_length)
        print(possible_word, file=sys.stderr)
        if not possible_word or possible_word.name in puzzle_words['Word']:
            print('redoing', file=sys.stderr)
            keys_list = word_keys + keys_list
        else:
            puzzle_words['Word'].append(possible_word.name)
            puzzle_words['Keys'].append(word_keys)
            puzzle_words['Length'].append(possible_word.length)
    pw = ','.join(puzzle_words['Word'])
    kw = ';'.join([','.join(k) for k in puzzle_words['Keys']])
    new_puzzle = Puzzle(question=question, answer=answer, words=pw, letter_keys=kw)
    db.session.add(new_puzzle)
    db.session.commit()
    return 'Created Puzzle', new_puzzle.id


def shuffle_word(word):
    sw = list(word)
    while ''.join(sw) == word:
        shuffle(sw)
    return ''.join(sw)


def build_game(puzzle_id):
    game_puzzle = Puzzle.query.filter_by(id=puzzle_id).first()
    if not game_puzzle:
        return 'Puzzle no existo?', None

    question = game_puzzle.question
    answer = game_puzzle.answer
    words = game_puzzle.words.split(',')
    scrambled_words = [shuffle_word(word) for word in words]
    key_letters = [enumerate(kw.split(',')) for kw in game_puzzle.letter_keys.split(';')]

    new_game = {'id': game_puzzle.id, 'question': question, 'answer': answer, 'words': words,
                'key_letters': key_letters, 'scrambled_words': enumerate(scrambled_words)}

    return 'success', new_game
