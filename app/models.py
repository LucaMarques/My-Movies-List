from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

"""
class Filme(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    episodios = db.relationship('Episodio', backref='filme', lazy=True)"""


class Episodio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    numero = db.Column(db.String(10), nullable=False)
    avaliacao = db.Column(db.Float, default=0.0)
    #filme_id = db.Column(db.Integer, db.ForeignKey('filme.id'), nullable=False)

    def __repr__(self):
        return f"<Episodio {self.numero} - {self.titulo}>"