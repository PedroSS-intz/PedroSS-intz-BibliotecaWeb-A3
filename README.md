Sistema web de gerenciamento de biblioteca desenvolvido
como atividade acadêmica da disciplina de Garantia da
Qualidade de Software - A3 (2026/2).

Objetivo:
Permitir o gerenciamento de livros, empréstimos e devoluções,
aplicando técnicas de Garantia da Qualidade de Software.

Funcionalidade
- Cadastro de livros com validação dos dados.
- Consulta e pesquisa de livros por título ou autor.
- Registro de empréstimos.
- Controle de disponibilidade dos exemplares.
- Registro de devoluções.
- Validação de operações inválidas.

Ferramentas:
- Python
- Flask
- SQLite
- HTML e CSS
- pytest
- Selenium WebDriver
- Git e GitHub


Requisitos
- Python instalado (projeto testado com Python 3.15).
- Google Chrome instalado.
- Terminal PowerShell no Windows.


Abra um terminal na pasta BibliotecaWeb.
Ambiente virtual:

```powershell
python -m venv .venv
```

Instale as dependências:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Executar:

No terminal, execute:

```powershell
.\.venv\Scripts\python.exe app.py
```

Acesse:

http://127.0.0.1:5000

O banco de dados principal será criado automaticamente.

Testes:
Para executar os testes das regras de negócio:

```powershell
.\.venv\Scripts\python.exe -m pytest -v tests/test_regras.py
```

Foram implementados 12 testes automatizados de validação.

Selenium:

Os testes Selenium utilizam um banco separado do banco principal.

Abra o primeiro terminal e execute:

```powershell
$env:BIBLIOTECA_BANCO = "biblioteca_teste.db"
.\.venv\Scripts\python.exe banco.py
.\.venv\Scripts\python.exe -m flask --app app run --port 5001 --no-reload
```

Mantenha esse terminal aberto.

Em um segundo terminal, execute:

```powershell
.\.venv\Scripts\python.exe -m pytest -v tests/test_selenium.py
```

O Selenium utilizará o Chrome para automatizar quatro cenários,
incluindo cadastro, consulta, validação e empréstimo.

Banco de Dados:
biblioteca.db:
Banco principal utilizado pela aplicação.

biblioteca_teste.db:
Banco utilizado nos testes de interface.

Os arquivos de banco de dados são ignorados pelo Git


Limitações:
Utiliza servidor local de desenvolvimento e sem
autenticação de usuários.

Os testes Selenium precisam do Chrome e da aplicação
de testes na porta 5001.

Equipe:
Pedro de Sousa Cuneo
Luana Princes Leocadio Machado
Augusto Perim 
