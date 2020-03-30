from app import db


class Word(db.Model):
    """list of words for use"""
    __tablename__ = 'words'
    id = db.Column(db.Integer, primary_key=True)
    length = db.Column(db.Integer, index=True)
    category = db.Column(db.VARCHAR(128))
    letters = db.Column(db.VARCHAR(128), index=True)
    name = db.Column(db.VARCHAR(128), nullable=False, index=True)

    def __repr__(self):
        return self.name


class Puzzle(db.Model):
    """the puzzle created"""
    __tablename__ = 'puzzles'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.VARCHAR(128), nullable=False)
    answer = db.Column(db.VARCHAR(128), nullable=False)
    words = db.Column(db.VARCHAR(128), nullable=False)
    letter_keys = db.Column(db.VARCHAR(128), nullable=False)

    def __repr__(self):
        return self.question+': '+self.answer
