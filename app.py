from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for
)

from banco import criar_tabelas

from livros import (
    cadastrar_livro,
    listar_livros,
    emprestar_livro,
    listar_emprestimos_ativos,
    devolver_livro
)


app = Flask(__name__)

criar_tabelas()


@app.route("/")
def pagina_inicial():
    return render_template("index.html")


@app.route("/cadastrar", methods=["GET", "POST"])
def pagina_cadastro():
    erro = None

    if request.method == "POST":
        try:
            cadastrar_livro(
                request.form.get("titulo", ""),
                request.form.get("autor", ""),
                request.form.get("quantidade", "")
            )

            return redirect(
                url_for("pagina_cadastro", sucesso=1)
            )

        except ValueError as excecao:
            erro = str(excecao)

    return render_template(
        "cadastrar.html",
        erro=erro,
        sucesso=request.args.get("sucesso") == "1"
    )


@app.route("/livros")
def pagina_consulta():
    termo = request.args.get("q", "").strip()

    livros = listar_livros(termo)

    return render_template(
        "consultar.html",
        livros=livros,
        termo=termo
    )

@app.route("/emprestimos", methods=["GET", "POST"])
def pagina_emprestimos():
    erro = None

    if request.method == "POST":
        try:
            emprestar_livro(
                request.form.get("livro_id", ""),
                request.form.get("nome_leitor", "")
            )

            return redirect(
                url_for("pagina_emprestimos", sucesso=1)
            )

        except ValueError as excecao:
            erro = str(excecao)

    return render_template(
        "emprestimos.html",
        livros=listar_livros(),
        emprestimos=listar_emprestimos_ativos(),
        erro=erro,
        sucesso=request.args.get("sucesso") == "1"
    )


@app.route("/devolucoes", methods=["GET", "POST"])
def pagina_devolucoes():
    erro = None

    if request.method == "POST":
        try:
            devolver_livro(
                request.form.get("emprestimo_id", "")
            )

            return redirect(
                url_for("pagina_devolucoes", sucesso=1)
            )

        except ValueError as excecao:
            erro = str(excecao)

    return render_template(
        "devolucoes.html",
        emprestimos=listar_emprestimos_ativos(),
        erro=erro,
        sucesso=request.args.get("sucesso") == "1"
    )



if __name__ == "__main__":
    app.run(debug=True)
