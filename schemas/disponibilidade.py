from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from model.disponibilidade import Disponibilidade


class DisponibilidadeSchema(BaseModel):
    """ Define como uma nova disponibilidade a ser inserida deve ser representada
    """
    programa: str = "Breaking Bad"
    tipo: str = "Série"
    temporadas: int = 5
    plataforma: str = "Netflix"
    pais: str = "Brasil"
    temporadas_disponiveis: str = "1,2,3,4,5"
    data_limite: str = "2025-12-31"
    link: str = "https://www.netflix.com/title/70143836"



class DispProgLocalBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca por programa local. Que será
        feita com base no nome do programa e do pais.
    """
    programa: str = "Breaking Bad"
    pais: str = "Brasil"

class DisponibilidadeBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita com base no programa, plataforma e pais.
    """
    programa: str = "Breaking Bad"
    plataforma: str = "Netflix"
    pais: str = "Brasil"

class ListagemDisponibilidadesSchema(BaseModel):
    """ Define como uma listagem de Disponibilidades será retornada.
    """
    disponibilidades:List[DisponibilidadeSchema]


def apresenta_disponibilidades(disponibilidades: List[Disponibilidade]):
    """ Retorna uma representação de uma lista de disponibilidades seguindo o schema definido em
        DisponibilidadeViewSchema.
    """
    result = []
    for disponibilidade in disponibilidades:
        result.append({
            "programa": disponibilidade.programa,
            "tipo": disponibilidade.tipo,
            "temporadas": disponibilidade.temporadas,
            "plataforma": disponibilidade.plataforma,
            "pais": disponibilidade.pais,
            "temporadas_disponiveis": disponibilidade.temporadas_disponiveis,
            "data_limite": disponibilidade.data_limite.strftime('%d/%m/%Y'),
            "link": disponibilidade.link,
        })

    return {"disponibilidades": result}


class DisponibilidadeViewSchema(BaseModel):
    """ Define como uma disponibilidade será retornada
    """
    id: int = 1
    programa: str = "Breaking Bad"
    tipo: str = "Série"
    temporadas: int = 5
    plataforma: str = "Netflix"
    pais: str = "Brasil"
    temporadas_disponiveis: str = "1,2,3,4,5"
    data_limite: datetime = datetime.strptime('2025-12-31', '%Y-%m-%d')
    link: str = "https://www.netflix.com/title/70143836"


class DisponibilidadeDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    programa: str
    plataforma: str
    pais: str

def apresenta_disponibilidade(disponibilidade: Disponibilidade):
    """ Retorna uma representação da disponibilidade seguindo o schema definido em
        DisponibilidadeViewSchema.
    """
    return {
        "programa": disponibilidade.programa,
        "tipo": disponibilidade.tipo,
        "temporadas": disponibilidade.temporadas,
        "plataforma": disponibilidade.plataforma,
        "pais": disponibilidade.pais,
        "temporadas_disponiveis": disponibilidade.temporadas_disponiveis,
        "data_limite": disponibilidade.data_limite.strftime('%d/%m/%Y'),
        "link": disponibilidade.link,
    }
