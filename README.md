Este projeto é uma demo utilizando o FastAPI, um framework web moderno e de alta performance para a construção de APIs com Python 3.7 ou superior.

Para rodar localmente, siga os passos abaixo:

1. Certifique-se de que o `virtualenv` está instalado. Caso não esteja, instale com o comando:

   ```bash
   pip install virtualenv
   ```

2. Crie um ambiente virtual com o comando:

   ```bash
   python -m virtualenv venv
   ```

3. Ative o ambiente virtual:

   - No Linux/macOS:

     ```bash
     source venv/bin/activate
     ```

   - No Windows (CMD):

     ```cmd
     venv\Scripts\activate.bat
     ```

   - No Windows (PowerShell):

     ```powershell
     venv\Scripts\Activate.ps1
     ```

4. Com o ambiente virtual ativado, instale as dependências do projeto utilizando o arquivo `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

5. Execute o servidor FastAPI com Uvicorn usando o comando abaixo:

   ```bash
   uvicorn main:app --reload
   ```

   > Substitua `main` pelo nome do seu arquivo Python principal, se for diferente de `main.py`. No caso do `main.py` disponivel dentro da pasta Project seria

     ```bash
   uvicorn Product.main:app --reload
   ```


   O parâmetro `--reload` faz com que o servidor reinicie automaticamente sempre que houver alterações no código, o que é útil durante o desenvolvimento.

6. Com o servidor rodando, acesse no navegador:

    > O `main.py` no arquivo raiz:
   - Documentação Swagger: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - Documentação ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

   > O `main.py` na pasta Product:
   - Documentação Swagger: [http://127.0.0.1:8000/docdocumentacao](http://127.0.0.1:8000/documentacao)
   - Documentação ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

Esses endpoints são gerados automaticamente pelo FastAPI com base nas rotas definidas na aplicação.

