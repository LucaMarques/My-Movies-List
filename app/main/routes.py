from . import main
from flask import render_template, request, redirect, url_for, session, flash, jsonify # type: ignore
from app.models import db, Filme, Usuario
from flask_login import login_required, current_user, login_user, logout_user


# Pagina inicial
@main.route('/')
def index():
    filmes = Filme.query.limit(4).all()
    return render_template("index.html",filmes=filmes)

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
    if current_user.is_authenticated:
        return redirect(url_for('main.perfil'))
    if request.method == "POST":
        usuario = request.form["usuario"]
        senha = request.form["senha"]

        user = Usuario.query.filter_by(usuario=usuario).first()

        if user and user.verificar_senha(senha):
            session["usuario_id"] = user.id
            login_user(user)
            flash("Login realizado com sucesso!")
            return redirect(url_for("main.index")) 
        else:
            flash("Usuário ou senha inválidos.")
            return redirect(url_for("main.login"))

    return render_template("login.html")

# Pagina de logout
@main.route("/logout")
def logout():
    session.pop("usuario_id", None)
    logout_user()
    flash("Logout realizado com sucesso.")
    return redirect(url_for("main.login"))

# Pagina perfil
@main.route("/perfil")
@login_required
def perfil():
    if not current_user.is_authenticated:
        flash("Você precisa estar logado para ver essa página.")
        return redirect(url_for("main.login"))

    usuario = Usuario.query.get(session["usuario_id"])
    return render_template("perfil.html", usuario=usuario)

@main.route('/editar-perfil', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        current_user.nome = request.form.get('nome', current_user.nome)
        current_user.usuario = request.form.get('usuario', current_user.usuario)
        current_user.foto_url = request.form.get('foto_url', current_user.foto_url)
        current_user.descricao = request.form.get('descricao', current_user.descricao)
        db.session.add(current_user)
        db.session.commit()
        flash('Perfil atualizado!')
        return redirect(url_for('main.perfil'))

    return render_template('editar_perfil.html', usuario=current_user)

@main.route("/sugestoes")
def sugestoes():
    termo = request.args.get("q", "")
    if not termo:
        return jsonify([])

    filmes = Filme.query.filter(Filme.titulo.ilike(f"%{termo}%")).limit(5).all()
    return jsonify([{"id": f.id, "titulo": f.titulo} for f in filmes])
