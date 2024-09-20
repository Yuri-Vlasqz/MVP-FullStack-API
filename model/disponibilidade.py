from sqlalchemy import Column, String, Integer, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime

from  model import Base


class Disponibilidade(Base):
    __tablename__ = 'disponibilidade'

    id = Column("pk_disp", Integer, primary_key=True)
    programa = Column(String(100), nullable=False)
    tipo = Column(String(5), nullable=False)  # valores possiveis: série, filme
    temporadas = Column(Integer, nullable=False)  # duração para filmes
    plataforma = Column(String(100), nullable=False)
    pais = Column(String(100), nullable=False)
    temporadas_disponiveis = Column(String(100), nullable=True) # nulos para filmes
    data_limite = Column(DateTime, nullable=False)
    link = Column(String(100), nullable=False)

    # Definição para assegurar unicidade para multiplas colunas
    __table_args__ = (UniqueConstraint('programa', 'plataforma', 'pais', name='_prog_plat_local'),)

    def __init__(self, programa:str, tipo: str, temporadas:int, plataforma:str, pais:str, temporadas_disponiveis:str, data_limite:str, link:str):
        """
        Cria uma Disponibilidade

        Arguments:
            programa: nome do programa.
            tipo: tipo de programa (serie ou filme)
            temporadas: quantidade de temporadas (0 para filmes)
            plataforma: nome da plataforma de streaming
            pais: pais da plataforma de streaming
            temporadas_disponiveis: numero das temporadas disponiveis TODO: extra transformar em lista
            data_limite: data final de diponibilidade na platforma local (formato dd/mm/aaaa)
            link: link do programa na plataforma local
        """
        self.programa = programa
        self.tipo = tipo
        self.temporadas = temporadas
        self.plataforma = plataforma
        self.pais = pais
        self.temporadas_disponiveis = temporadas_disponiveis
        self.data_limite = datetime.strptime(data_limite, '%Y-%m-%d')
        self.link = link

