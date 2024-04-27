from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base, Comentario


class Planejamento(Base):
    __tablename__ = 'planejamento'

    id = Column("pk_planejamento", Integer, primary_key=True)
    encarregado = Column(String(140), unique=True)
    equipe = Column(String(140))
    funcao = Column(String(140))
    servico_local = Column(String(140))
    data_insercao = Column(DateTime, default=datetime.now())

    # Definição do relacionamento entre o planejamento e o comentário.
    # Essa relação é implicita, não está salva na tabela 'planejamento',
    # mas aqui estou deixando para SQLAlchemy a responsabilidade
    # de reconstruir esse relacionamento.
    comentarios = relationship('Comentario')

    def __init__(self, encarregado:str, equipe:str, funcao:str,
                 servico_local:str, data_insercao: Union[DateTime, None] = None):
        """
        Cria um Planejamento

        Arguments:
            encarregado: encarregado responsável pelo planejamento.
            equipe: equipe responsável por executar o serviço.
            funcao: cargo de cada membro da equipe.
            servico_local: servico a ser executado e o local na obra.
            data_insercao: data de quando o planejamento foi inserido à base
        """
        self.encarregado = encarregado
        self.equipe = equipe
        self.funcao = funcao
        self.servico_local = servico_local
        
        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao

    def adiciona_comentario(self, comentario:Comentario):
        """ Adiciona um novo comentário ao Planejamento
        """
        self.comentarios.append(comentario)

