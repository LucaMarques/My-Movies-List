from . import main
from datetime import datetime
from flask import render_template, request, redirect, url_for, session, flash, jsonify
from app.models import db, Ator, Filme, Atuacao, Episodio, Genero, Usuario


# Pagina inicial
@main.route('/')
def index():
    return render_template("index.html")

# Pagina de filmes/series
@main.route('/series/<int:filme_id>')
def series(filme_id):
    filme = Filme.query.get_or_404(filme_id)
    episodios = filme.episodios
    atuacoes = filme.atuacoes

    return render_template('film-page.html', filme=filme, episodios=episodios, elenco=atuacoes)


# Formulário de cadastro
@main.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form["nome"]
        usuario = request.form["usuario"]
        senha = request.form["senha"]

        if Usuario.query.filter_by(usuario=usuario).first():
            flash("Nome de usuário já está em uso.")
            return redirect(url_for("main.cadastro"))

        novo_usuario = Usuario(nome=nome, usuario=usuario)
        novo_usuario.set_senha(senha)

        db.session.add(novo_usuario)
        db.session.commit()

        flash("Cadastro realizado com sucesso. Faça login.")
        return redirect(url_for("main.login"))

    return render_template("cadastro.html")

# Formulário de login
@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        senha = request.form["senha"]

        usuario_db = Usuario.query.filter_by(usuario=usuario).first()

        if usuario_db and usuario_db.verificar_senha(senha):
            session["usuario_id"] = usuario_db.id
            flash("Login realizado com sucesso!")
            return redirect(url_for("main.index"))  # Altere conforme sua rota principal
        else:
            flash("Usuário ou senha inválidos.")
            return redirect(url_for("main.login"))

    return render_template("login.html")


@main.route("/logout")
def logout():
    session.pop("usuario_id", None)
    flash("Logout realizado com sucesso.")
    return redirect(url_for("main.login"))

@main.route("/perfil")
def perfil():
    if "usuario_id" not in session:
        flash("Você precisa estar logado para ver essa página.")
        return redirect(url_for("main.login"))

    usuario = Usuario.query.get(session["usuario_id"])
    return render_template("perfil.html", usuario=usuario)

@main.route("/sugestoes")
def sugestoes():
    termo = request.args.get("q", "")
    if not termo:
        return jsonify([])

    filmes = Filme.query.filter(Filme.titulo.ilike(f"%{termo}%")).limit(5).all()
    return jsonify([{"id": f.id, "titulo": f.titulo} for f in filmes])
