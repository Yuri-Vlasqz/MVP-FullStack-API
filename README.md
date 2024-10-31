# MVP Full Stack - Backend (API)

Este repositório contém a implementação do back-end do **MVP** (_Minimum Viable Product_) da _Sprint_ de **Desenvolvimento _Full Stack_ Básico** do Curso de Engenharia de Software da PUC-Rio. A API foi construída utilizando `Flask`, documentada por `Swagger`, e o banco de dados foi modelado com `SQLAlchemy`. A parte do front-end pode ser acessada em [MVP-FullStack-Frontend](https://github.com/Yuri-Vlasqz/MVP-FullStack-Frontend).

No contexto da crescente variedade de serviços de streaming e a variação de conteúdo de acordo com a localização geográfica, pode ser difícil para os usuários identificar quais programas estão disponíveis em sua região.

> O projeto completo consiste em uma aplicação web que permite aos usuários buscar séries e filmes disponíveis em plataformas de _streaming_ de um país específico. Além disso, oferece funcionalidades de cadastro, deleção e listagem de programas de TV em um banco de dados local.

### Principais rotas da API:

1. **Adição de uma Disponibilidade:** `POST/disponibilidade` 

2. **Deleção de uma Disponibilidade:** `DEL/disponibilidade`

3. **Listagem de todas Disponibilidades:** `GET/disponibilidades`

3. **Busca de Disponibilidades por programa e país:** `GET/disponibilidade`

<br>

## Como executar 

1. Clone este repositório pela URL.

2. No diretório raiz do repositório, pelo terminal, execute o comando abaixo para criar um ambiente virtual do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).
    ```
    python -m venv .venv
    ```
    
3. Ative o ambiente virtual.
    ```
    .venv\Scripts\activate.ps1
    ```

4. Instale todas as dependências/bibliotecas python listadas no `requirements.txt` no ambiente virtual. 
    > Versão python utilizada: 3.12.3
    ```
    pip install -r requirements.txt
    ```


5. Execute a API:
    ```
    flask run --host 0.0.0.0 --port 5000
    ```

    Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
    automaticamente após uma mudança no código fonte. 

    ```
    flask run --host 0.0.0.0 --port 5000 --reload
    ```

6. Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar a documentação em `Swagger` e o status da API em execução.
