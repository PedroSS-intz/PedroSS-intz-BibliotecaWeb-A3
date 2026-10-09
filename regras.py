def validar_cadastro(titulo, autor, quantidade_texto):
    titulo = (titulo or "").strip()
    autor = (autor or "").strip()

    if not titulo:
        raise ValueError("O título é obrigatório.")

    if not autor:
        raise ValueError("O autor é obrigatório.")

    try:
        quantidade = int(quantidade_texto)
    except (ValueError, TypeError):
        raise ValueError(
            "A quantidade deve ser um número inteiro."
        ) from None

    if quantidade <= 0:
        raise ValueError(
            "A quantidade deve ser maior que zero."
        )

    return titulo, autor, quantidade


def validar_leitor(nome_leitor):
    nome_leitor = (nome_leitor or "").strip()

    if not nome_leitor:
        raise ValueError("Informe o nome do leitor.")

    return nome_leitor


def validar_disponibilidade(quantidade_disponivel):
    if quantidade_disponivel <= 0:
        raise ValueError(
            "Este livro não possui exemplares disponíveis."
        )


def validar_devolucao(data_devolucao):
    if data_devolucao is not None:
        raise ValueError(
            "Este empréstimo já foi devolvido."
        )
