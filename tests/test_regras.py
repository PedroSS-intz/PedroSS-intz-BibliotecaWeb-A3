
import pytest

from regras import (
    validar_cadastro,
    validar_leitor,
    validar_disponibilidade,
    validar_devolucao
)


# TESTES DE CADASTRO

def test_cadastro_aceita_dados_validos():
    resultado = validar_cadastro(
        "Dom Casmurro",
        "Machado de Assis",
        "3"
    )

    assert resultado == (
        "Dom Casmurro",
        "Machado de Assis",
        3
    )


def test_cadastro_rejeita_titulo_vazio():
    with pytest.raises(ValueError, match="título é obrigatório"):
        validar_cadastro("", "Machado de Assis", "3")


def test_cadastro_rejeita_autor_vazio():
    with pytest.raises(ValueError, match="autor é obrigatório"):
        validar_cadastro("Dom Casmurro", "", "3")


def test_cadastro_rejeita_quantidade_zero():
    with pytest.raises(ValueError, match="maior que zero"):
        validar_cadastro("Dom Casmurro", "Machado", "0")


def test_cadastro_rejeita_quantidade_nao_numerica():
    with pytest.raises(ValueError, match="número inteiro"):
        validar_cadastro("Dom Casmurro", "Machado", "abc")


def test_cadastro_rejeita_quantidade_negativa():
    with pytest.raises(ValueError, match="maior que zero"):
        validar_cadastro("Dom Casmurro", "Machado", "-5")


# TESTES DE IDENTIFICACAO DO LEITOR

def test_leitor_aceita_nome_valido():
    resultado = validar_leitor("  Pedro  ")

    assert resultado == "Pedro"


def test_leitor_rejeita_nome_vazio():
    with pytest.raises(ValueError, match="nome do leitor"):
        validar_leitor("   ")


# TESTES DE DISPONIBILIDADE

def test_emprestimo_aceita_estoque_disponivel():
    resultado = validar_disponibilidade(3)

    assert resultado is None


def test_emprestimo_rejeita_estoque_zerado():
    with pytest.raises(ValueError, match="não possui exemplares"):
        validar_disponibilidade(0)


# TESTES DE DEVOLUCAO

def test_devolucao_aceita_emprestimo_ativo():
    resultado = validar_devolucao(None)

    assert resultado is None


def test_devolucao_rejeita_emprestimo_ja_devolvido():
    with pytest.raises(ValueError, match="já foi devolvido"):
        validar_devolucao("2026-10-09 15:00:00")
