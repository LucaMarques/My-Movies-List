from flask_sqlalchemy import SQLAlchemy
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

filme_genero = db.Table('filme_genero',
    db.Column('genero_id', db.Integer, db.ForeignKey('genero.id'), primary_key=True),
    db.Column('filme_id', db.Integer, db.ForeignKey('filme.id'), primary_key=True)
)

usuario_filme_fav = db.Table('usuario_filme_fav',
    db.Column('usuario_id', db.Integer, db.ForeignKey('usuario.id'), primary_key=True),
    db.Column('filme_id', db.Integer, db.ForeignKey('filme.id'), primary_key=True)
)

usuario_filme_assistindo = db.Table('usuario_filme_assistindo',
    db.Column('usuario_id', db.Integer, db.ForeignKey('usuario.id'), primary_key=True),
    db.Column('filme_id', db.Integer, db.ForeignKey('filme.id'), primary_key=True)
)

class Filme(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    temporada = db.Column(db.Integer, nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    trailer = db.Column(db.String(100), nullable=True)

    episodios = db.relationship('Episodio', backref='filme', lazy=True)
    atuacoes = db.relationship("Atuacao", back_populates='filme', cascade='all, delete-orphan')
    generos = db.relationship('Genero', secondary=filme_genero, back_populates='filmes')

    @property
    def media(self):
        if self.episodios:
            media = sum(nota.avaliacao for nota in self.episodios) / len(self.episodios)
            media = round(media, 1)
            return media
        else:
            media = None
        return media

class Episodio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    numero = db.Column(db.String(10), nullable=False)
    filme_id = db.Column(db.Integer, db.ForeignKey('filme.id', name='fk_episodio_filme_id'), nullable=False)

    avaliacoes = db.relationship('Avaliacao', back_populates='episodio', cascade='all, delete-orphan')

    @property
    def media(self):
        if self.avaliacoes:
            total = sum(av.nota for av in self.avaliacoes)
            media = total / len(self.avaliacoes)
            return round(media, 1)
        return None

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

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(100), nullable=False)
    usuario = db.Column(db.String(50), unique=True, nullable=False)
    senha_hash = db.Column(db.String(100), nullable=False)
    foto_url = db.Column(db.String(100), nullable=True)
    descricao = db.Column(db.Text, nullable=True)

    filmes_fav = db.relationship('Filme',
        secondary=usuario_filme_fav,
        backref=db.backref('usuarios_favoritaram', lazy='dynamic'),
        lazy='dynamic')

    assistindo = db.relationship('Filme',
        secondary=usuario_filme_assistindo,
        backref=db.backref('usuarios_assistindo', lazy='dynamic'),
        lazy='dynamic')

    avaliacoes = db.relationship('Avaliacao', back_populates='usuario', cascade='all, delete-orphan')

    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def verificar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

class Avaliacao(db.Model):
    __tablename__ = 'avaliacao'
    
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), primary_key=True)
    episodio_id = db.Column(db.Integer, db.ForeignKey('episodio.id'), primary_key=True)
    nota = db.Column(db.Float, nullable=False)

    usuario = db.relationship('Usuario', back_populates='avaliacoes')
    episodio = db.relationship('Episodio', back_populates='avaliacoes')