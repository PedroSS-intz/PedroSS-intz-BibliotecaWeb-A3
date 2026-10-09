
import os
import sqlite3
from pathlib import Path

CAMINHO_BANCO = (
    Path(__file__).resolve().parent
    / os.environ.get("BIBLIOTECA_BANCO", "biblioteca.db")
)


def criar_tabelas():
    conexao = sqlite3.connect(CAMINHO_BANCO)

    try:
        conexao.execute("""
            CREATE TABLE IF NOT EXISTS livros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                autor TEXT NOT NULL,
                quantidade_total INTEGER NOT NULL
                    CHECK (quantidade_total >= 1),
                quantidade_disponivel INTEGER NOT NULL
                    CHECK (
                        quantidade_disponivel >= 0
                        AND quantidade_disponivel <= quantidade_total
                    )
            )
        """)

        conexao.execute("""
            CREATE TABLE IF NOT EXISTS emprestimos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                livro_id INTEGER NOT NULL,
                nome_leitor TEXT NOT NULL,
                data_emprestimo TEXT NOT NULL
                    DEFAULT CURRENT_TIMESTAMP,
                data_devolucao TEXT,

                FOREIGN KEY (livro_id)
                    REFERENCES livros(id)
            )
        """)

        conexao.commit()

    finally:
        conexao.close()


if __name__ == "__main__":
    criar_tabelas()
    print("Banco de dados criado com sucesso!")
