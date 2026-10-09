import pytest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

import sqlite3
from uuid import uuid4

from pathlib import Path

CAMINHO_BANCO = (
    Path(__file__).resolve().parents[1]
    / "biblioteca_teste.db"
)

from selenium.common.exceptions import StaleElementReferenceException


URL_BASE = "http://127.0.0.1:5001"


@pytest.fixture
def navegador():
    driver = webdriver.Chrome()
    driver.set_window_size(1280, 900)

    yield driver

    driver.quit()


def test_cadastro_sem_titulo_exibe_erro(navegador):
    # Abrir a página de cadastro
    navegador.get(f"{URL_BASE}/cadastrar")

    # Preencher o autor
    navegador.find_element(
        By.ID, "autor"
    ).send_keys("Machado de Assis")

    # Informar a quantidade
    navegador.find_element(
        By.ID, "quantidade"
    ).send_keys("3")

    # Deixar o título vazio e clicar em cadastrar
    navegador.find_element(
        By.CSS_SELECTOR, 'button[type="submit"]'
    ).click()

    # Aguardar a mensagem de erro aparecer
    mensagem = WebDriverWait(navegador, 10).until(
        EC.visibility_of_element_located(
            (By.CLASS_NAME, "erro")
        )
    )

    # Confirmar que o sistema rejeitou o cadastro
    assert "O título é obrigatório." in mensagem.text



def test_cadastro_valido_aparece_na_consulta(navegador):

    # Criar um título único para cada execução
    titulo = f"Livro Selenium {uuid4().hex[:8]}"

    try:
        # Abrir a página de cadastro
        navegador.get(f"{URL_BASE}/cadastrar")

        # Preencher o título
        navegador.find_element(
            By.ID, "titulo"
        ).send_keys(titulo)

        # Preencher o autor
        navegador.find_element(
            By.ID, "autor"
        ).send_keys("Autor Automatizado")

        # Informar a quantidade
        navegador.find_element(
            By.ID, "quantidade"
        ).send_keys("2")

        # Confirmar o cadastro
        navegador.find_element(
            By.CSS_SELECTOR, 'button[type="submit"]'
        ).click()

        # Verificar a mensagem de sucesso
        mensagem = WebDriverWait(navegador, 10).until(
            EC.visibility_of_element_located(
                (By.CLASS_NAME, "sucesso")
            )
        )

        assert "Livro cadastrado com sucesso!" in mensagem.text

        # Abrir a página de consulta
        navegador.get(f"{URL_BASE}/livros")

        # Pesquisar pelo livro cadastrado
        navegador.find_element(
            By.ID, "q"
        ).send_keys(titulo)

        navegador.find_element(
            By.CSS_SELECTOR, 'button[type="submit"]'
        ).click()

        # Aguardar a navegacao terminar apos clicar em Pesquisar.
        WebDriverWait(navegador, 10).until(
            EC.url_contains("/livros?q=")
        )

        # Verificar o titulo diretamente na tabela atual.
        # A espera localiza novamente o elemento se a pagina recarregar.
        assert WebDriverWait(navegador, 10).until(
            EC.text_to_be_present_in_element(
                (By.CSS_SELECTOR, "tbody"),
                titulo
            )
        )

    finally:
        # Remover somente o livro criado pelo teste
        with sqlite3.connect(CAMINHO_BANCO) as conexao:
            conexao.execute(
                "DELETE FROM livros WHERE titulo = ?",
                (titulo,)
            )

            
def test_pesquisa_livro_inexistente(navegador):

    # Gerar um titulo que nao existe no banco
    titulo = f"Inexistente_{uuid4().hex}"

    # Abrir a pagina de consulta
    navegador.get(f"{URL_BASE}/livros")

    # Digitar o titulo na pesquisa
    navegador.find_element(
        By.ID, "q"
    ).send_keys(titulo)

    # Clicar no botao pesquisar
    navegador.find_element(
        By.CSS_SELECTOR, 'button[type="submit"]'
    ).click()

    # Aguardar a pagina de resultados
    WebDriverWait(navegador, 10).until(
        EC.url_contains("/livros?q=")
    )

    # Verificar a mensagem de nenhum resultado
    mensagem = WebDriverWait(navegador, 10).until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "//p[normalize-space()='Nenhum livro encontrado.']"
            )
        )
    )

    assert mensagem.text == "Nenhum livro encontrado."


def test_emprestimo_reduz_disponibilidade(navegador):

    # Criar dados exclusivos para este teste
    titulo = f"Emprestimo Selenium {uuid4().hex[:8]}"
    leitor = f"Leitor Teste {uuid4().hex[:8]}"

    try:
        # ETAPA 1: Cadastrar um livro com 1 exemplar
        navegador.get(f"{URL_BASE}/cadastrar")

        navegador.find_element(
            By.ID, "titulo"
        ).send_keys(titulo)

        navegador.find_element(
            By.ID, "autor"
        ).send_keys("Autor Selenium")

        navegador.find_element(
            By.ID, "quantidade"
        ).send_keys("1")

        navegador.find_element(
            By.CSS_SELECTOR, 'button[type="submit"]'
        ).click()

        # Confirmar que o cadastro funcionou
        WebDriverWait(navegador, 10).until(
            EC.visibility_of_element_located(
                (By.CLASS_NAME, "sucesso")
            )
        )

        # ETAPA 2: Acessar a pagina de emprestimos
        navegador.get(f"{URL_BASE}/emprestimos")

        # Selecionar o livro criado pelo teste
        seletor = Select(
            navegador.find_element(By.ID, "livro_id")
        )

        opcao = next(
            item for item in seletor.options
            if titulo in item.text
        )

        seletor.select_by_value(
            opcao.get_attribute("value")
        )

        # Informar o nome do leitor
        navegador.find_element(
            By.ID, "nome_leitor"
        ).send_keys(leitor)

        # Confirmar o emprestimo
        navegador.find_element(
            By.CSS_SELECTOR, 'button[type="submit"]'
        ).click()

        # Verificar mensagem de sucesso
        mensagem = WebDriverWait(navegador, 10).until(
            EC.visibility_of_element_located(
                (By.CLASS_NAME, "sucesso")
            )
        )

        assert "Empréstimo realizado com sucesso!" in mensagem.text

        # ETAPA 3: Consultar o estoque do livro
        navegador.get(f"{URL_BASE}/livros")

        navegador.find_element(
            By.ID, "q"
        ).send_keys(titulo)

        navegador.find_element(
            By.CSS_SELECTOR, 'button[type="submit"]'
        ).click()

        # Aguardar a pesquisa terminar
        WebDriverWait(navegador, 10).until(
            EC.url_contains("/livros?q=")
        )

        # Verificar se a quantidade disponivel virou zero
        espera = WebDriverWait(
            navegador,
            10,
            ignored_exceptions=(StaleElementReferenceException,)
        )

        assert espera.until(
            lambda driver: driver.find_element(
                By.XPATH,
                f"//tbody/tr[td[normalize-space()='{titulo}']]/td[5]"
            ).text.strip() == "0"
        )

    finally:
        # Limpar os dados temporarios criados pelo teste
        with sqlite3.connect(CAMINHO_BANCO) as conexao:

            # Remover primeiro os emprestimos do livro
            conexao.execute(
                """
                DELETE FROM emprestimos
                WHERE livro_id IN (
                    SELECT id FROM livros WHERE titulo = ?
                )
                """,
                (titulo,)
            )

            # Remover o livro temporario
            conexao.execute(
                "DELETE FROM livros WHERE titulo = ?",
                (titulo,)
            )
