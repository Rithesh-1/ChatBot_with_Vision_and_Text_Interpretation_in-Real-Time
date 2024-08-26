#backend/models.py

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Query(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    question = db.Column(db.String(256),nullable = False)
    context_type= db.Column(db.String(64),nullable=False)
    context_source =db.Column(db.String(256),nullable =False)
    answer = db.Column(db.Text,nullable=False)
    