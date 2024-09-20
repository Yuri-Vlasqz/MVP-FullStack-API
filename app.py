from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Disponibilidade
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
disponibilidade_tag = Tag(name="Disponibilidade", description="Adição, visualização e remoção de disponibilidades à base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/disponibilidade', tags=[disponibilidade_tag],
          responses={"200": DisponibilidadeViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_disponibilidade(form: DisponibilidadeSchema):
    """Adiciona um nova disponibilidade à base de dados

    Retorna uma representação da disponibilidade.
    """
    disponibilidade = Disponibilidade(
        programa=form.programa,
        tipo=form.tipo,
        temporadas=form.temporadas,
        plataforma=form.plataforma,
        pais=form.pais,
        temporadas_disponiveis=form.temporadas_disponiveis,
        data_limite=form.data_limite,
        link=form.link,)
    logger.debug(f"Adicionando disponibilidade de programa: '{disponibilidade.programa}' na plataforma local: '{disponibilidade.plataforma} {disponibilidade.pais}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando disponibilidade
        session.add(disponibilidade)
        # efetivando o comando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado disponibilidade de programa: '{disponibilidade.programa}' na plataforma local: '{disponibilidade.plataforma} {disponibilidade.pais}'")
        return apresenta_disponibilidade(disponibilidade), 200

    except IntegrityError as e:
        # a duplicidade de programa, plataforma e país é a provável razão do IntegrityError
        error_msg = "Programa de mesmo nome já esta disponivel na plataforma local"
        logger.warning(f"Erro ao adicionar disponibilidade de programa '{disponibilidade.programa}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo programa :/"
        logger.warning(f"Erro ao adicionar disponibilidade de programa '{disponibilidade.programa}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.get('/disponibilidades', tags=[disponibilidade_tag],
         responses={"200": ListagemDisponibilidadesSchema, "404": ErrorSchema})
def get_disponibilidades():
    """Faz a busca por todos os disponibilidades cadastradas.
    
    Retorna uma representação da listagem de disponibilidades.
    """
    logger.debug(f"Coletando disponibilidades")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    disponibilidades = session.query(Disponibilidade).all()

    if not disponibilidades:
        # se não há disponibilidades cadastradas
        return {"disponibilidades": []}, 200
    else:
        logger.debug(f"{len(disponibilidades)} disponibilidades encontradas")
        # retorna a representação de disponibilidades
        return apresenta_disponibilidades(disponibilidades), 200


@app.get('/disponibilidade', tags=[disponibilidade_tag],
         responses={"200": ListagemDisponibilidadesSchema, "404": ErrorSchema})
def get_disponibilidade_programa_local(query: DispProgLocalBuscaSchema):
    """Faz a busca uma disponibilidade a partir do nome do programa e pais.

    Retorna uma representação das disponibilidade.
    """
    programa_nome = query.programa
    pais_nome = query.pais
    logger.debug(f"Coletando dados sobre programa {programa_nome} no {pais_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca (Case insensitive)
    disponibilidades = session.query(Disponibilidade).filter(Disponibilidade.programa.ilike(programa_nome), 
                                                             Disponibilidade.pais.ilike(pais_nome)).all()

    if not disponibilidades:
        # se disponibilidade não foi encontrada
        error_msg = "Disponibilidade não encontrado na base :/"
        logger.warning(f"Erro ao buscar programa '{programa_nome}' no {pais_nome}, {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Disponibilidade encontrada: '{programa_nome}' no {pais_nome}")
        # retorna a representação da lista de disponibilidades com programa e país
        return apresenta_disponibilidades(disponibilidades), 200


@app.delete('/disponibilidade', tags=[disponibilidade_tag],
            responses={"200": DisponibilidadeDelSchema, "404": ErrorSchema})
def del_disponibilidade(query: DisponibilidadeBuscaSchema):
    """Deleta um disponibiliade a partir do id informado.
    
    Retorna uma mensagem de confirmação da remoção.
    """
    programa_nome = unquote(unquote(query.programa))
    plataforma_nome = unquote(unquote(query.plataforma))
    pais_nome = unquote(unquote(query.pais))
    logger.debug(f"Deletando dados sobre programa {programa_nome} em {plataforma_nome} {pais_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Disponibilidade).filter(Disponibilidade.programa == programa_nome, 
                                                  Disponibilidade.plataforma == plataforma_nome, 
                                                  Disponibilidade.pais == pais_nome).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletando programa {programa_nome} em {plataforma_nome} {pais_nome}")
        return {"mesage": "Disponibilidade removida", "programa": programa_nome, "plataforma": plataforma_nome, "pais": pais_nome}
    else:
        # se o disponibilidade não foi encontrado
        error_msg = "Disponibilidade não encontrado na base :/"
        logger.warning(f"Erro ao deletar Disponibilidade de programa '{programa_nome}' em {plataforma_nome} {pais_nome}, {error_msg}")
        return {"mesage": error_msg}, 404
