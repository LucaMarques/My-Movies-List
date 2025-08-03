from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()

filme_genero = db.Table('filme_genero',
    db.Column('genero_id', db.Integer, db.ForeignKey('genero.id'), primary_key=True),
    db.Column('filme_id', db.Integer, db.ForeignKey('filme.id'), primary_key=True)
)

class Filme(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    temporada = db.Column(db.Integer)
    ano = db.Column(db.Integer)

    episodios = db.relationship('Episodio', backref='filme', lazy=True)
    atuacoes = db.relationship("Atuacao", back_populates='filme', cascade='all, delete-orphan')
    generos = db.relationship('Genero', secondary=filme_genero, back_populates='filmes')

    @property
    def media(self):
        if self.episodios:
            media = sum(ep.avaliacao for ep in self.episodios) / len(self.episodios)
            media = round(media, 1)
            return media
        else:
            media = None
        return media

class Episodio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    numero = db.Column(db.String(10), nullable=False)
    avaliacao = db.Column(db.Float, default=0.0)
    filme_id = db.Column(db.Integer, db.ForeignKey('filme.id', name='fk_episodio_filme_id'), nullable=False)

    def __repr__(self):
        return f"<Episodio {self.numero} - {self.titulo}>"
    
class Ator(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=True)

    atuacoes = db.relationship("Atuacao", back_populates='ator', cascade='all, delete-orphan')

    @property
    def idade(self):
        hoje = date.today()
        return hoje.year - self.data_nascimento.year - ((hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day))

class Atuacao(db.Model):
    __tablename__ = 'atuacao'

    ator_id = db.Column(db.Integer, db.ForeignKey('ator.id'), primary_key=True)
    filme_id = db.Column(db.Integer, db.ForeignKey('filme.id'), primary_key=True)
    personagem = db.Column(db.String(100), nullable=True)

    ator = db.relationship('Ator', back_populates='atuacoes')
    filme = db.relationship('Filme', back_populates='atuacoes')

class Genero(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(50), nullable=True)

    filmes = db.relationship('Filme', secondary=filme_genero, back_populates='generos')
