import sqlite3
from banco import CAMINHO_BANCO


from regras import (
    validar_cadastro,
    validar_leitor,
    validar_disponibilidade,
    validar_devolucao
)



def cadastrar_livro(titulo, autor, quantidade_texto):  
    titulo, autor, quantidade = validar_cadastro(
        titulo,
        autor,
        quantidade_texto
    )


    conexao = sqlite3.connect(CAMINHO_BANCO)

    try:
        cursor = conexao.execute(
            """
            INSERT INTO livros (
                titulo,
                autor,
                quantidade_total,
                quantidade_disponivel
            )
            VALUES (?, ?, ?, ?)
            """,
            (titulo, autor, quantidade, quantidade)
        )

        conexao.commit()
        return cursor.lastrowid

    finally:
        conexao.close()



def listar_livros(termo=""):
    termo = (termo or "").strip()

    conexao = sqlite3.connect(CAMINHO_BANCO)
    conexao.row_factory = sqlite3.Row

    try:
        sql = """
            SELECT
                id,
                titulo,
                autor,
                quantidade_total,
                quantidade_disponivel
            FROM livros
        """

        parametros = ()

        if termo:
            sql += """
                WHERE titulo LIKE ?
                   OR autor LIKE ?
            """
            parametros = (
                f"%{termo}%",
                f"%{termo}%"
            )

        sql += " ORDER BY titulo COLLATE NOCASE, id"

        cursor = conexao.execute(sql, parametros)

        return cursor.fetchall()

    finally:
        conexao.close()



def emprestar_livro(livro_id, nome_leitor):
    nome_leitor = validar_leitor(nome_leitor)

    try:
        livro_id = int(livro_id)
    except (ValueError, TypeError):
        raise ValueError(
            "Selecione um livro válido."
        ) from None

    if livro_id <= 0:
        raise ValueError("Selecione um livro válido.")

    conexao = sqlite3.connect(CAMINHO_BANCO)

    try:
        conexao.execute("PRAGMA foreign_keys = ON")
        conexao.execute("BEGIN IMMEDIATE")

        livro = conexao.execute(
            """
            SELECT quantidade_disponivel
            FROM livros
            WHERE id = ?
            """,
            (livro_id,)
        ).fetchone()

        if livro is None:
            raise ValueError("Livro não encontrado.")

        validar_disponibilidade(livro[0])

        conexao.execute(
            """
            UPDATE livros
            SET quantidade_disponivel =
                quantidade_disponivel - 1
            WHERE id = ?
            """,
            (livro_id,)
        )

        cursor = conexao.execute(
            """
            INSERT INTO emprestimos (
                livro_id,
                nome_leitor
            )
            VALUES (?, ?)
            """,
            (livro_id, nome_leitor)
        )

        conexao.commit()

        return cursor.lastrowid

    except Exception:
        conexao.rollback()
        raise

    finally:
        conexao.close()


def listar_emprestimos_ativos():
    conexao = sqlite3.connect(CAMINHO_BANCO)
    conexao.row_factory = sqlite3.Row

    try:
        cursor = conexao.execute(
            """
            SELECT
                emprestimos.id,
                livros.titulo,
                emprestimos.nome_leitor,
                emprestimos.data_emprestimo
            FROM emprestimos
            INNER JOIN livros
                ON livros.id = emprestimos.livro_id
            WHERE emprestimos.data_devolucao IS NULL
            ORDER BY emprestimos.id DESC
            """
        )

        return cursor.fetchall()

    finally:
        conexao.close()



def devolver_livro(emprestimo_id):
    try:
        emprestimo_id = int(emprestimo_id)
    except (ValueError, TypeError):
        raise ValueError(
            "Selecione um empréstimo válido."
        ) from None

    if emprestimo_id <= 0:
        raise ValueError(
            "Selecione um empréstimo válido."
        )

    conexao = sqlite3.connect(CAMINHO_BANCO)

    try:
        conexao.execute("PRAGMA foreign_keys = ON")
        conexao.execute("BEGIN IMMEDIATE")

        emprestimo = conexao.execute(
            """
            SELECT livro_id, data_devolucao
            FROM emprestimos
            WHERE id = ?
            """,
            (emprestimo_id,)
        ).fetchone()

        if emprestimo is None:
            raise ValueError(
                "Empréstimo não encontrado."
            )

        validar_devolucao(emprestimo[1])

        livro_id = emprestimo[0]

        conexao.execute(
            """
            UPDATE emprestimos
            SET data_devolucao = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (emprestimo_id,)
        )

        resultado = conexao.execute(
            """
            UPDATE livros
            SET quantidade_disponivel =
                quantidade_disponivel + 1
            WHERE id = ?
              AND quantidade_disponivel < quantidade_total
            """,
            (livro_id,)
        )

        if resultado.rowcount != 1:
            raise ValueError(
                "Não foi possível atualizar o estoque."
            )

        conexao.commit()

    except Exception:
        conexao.rollback()
        raise

    finally:
        conexao.close()