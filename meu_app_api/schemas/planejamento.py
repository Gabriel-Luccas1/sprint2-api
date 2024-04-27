from pydantic import BaseModel
from typing import List, Optional
from model.planejamento import Planejamento

from schemas import ComentarioSchema


class PlanejamentoSchema(BaseModel):
    """ Define como um novo planejamento a ser inserido deve ser representado
    """
    encarregado: str = "Pedro"
    equipe: str = "Gabriel e Lucas"
    funcao: str = "Pedreiro e ajudante"
    servico_local: str = "Reboco interno 402"


class PlanejamentoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do encarregado.
    """
    encarregado: str = ""


class ListagemPlanejamentosSchema(BaseModel):
    """ Define como uma listagem de planejamentos será retornada.
    """
    planejamentos:List[PlanejamentoSchema]


def apresenta_planejamentos(planejamentos: List[Planejamento]):
    """ Retorna uma representação do planejamento seguindo o schema definido em
        PlanejamentoViewSchema.
    """
    result = []
    for planejamento in planejamentos:
        result.append({
            "encarregado": planejamento.encarregado,
            "equipe": planejamento.equipe,
            "funcao": planejamento.funcao,
            "servico_local": planejamento.servico_local,
        })

    return {"planejamentos": result}


class PlanejamentoViewSchema(BaseModel):
    """ Define como um planejamento será retornado: planejamento + comentários.
    """
    id: int = 1
    encarregado: str = "Pedro"
    equipe: str = "Gabriel e Lucas"
    funcao: str = "Pedreiro e ajudante"
    servico_local: str = ""
    total_cometarios: int = 1
    comentarios:List[ComentarioSchema]


class PlanejamentoDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    encarregado: str

def apresenta_planejamento(planejamento: Planejamento):
    """ Retorna uma representação do planejamento seguindo o schema definido em
        PlanejamentoViewSchema.
    """
    return {
        "id": planejamento.id,
        "encarregado": planejamento.encarregado,
        "equipe": planejamento.equipe,
        "funcao": planejamento.funcao,
        "servico_local": planejamento.servico_local,
        "total_cometarios": len(planejamento.comentarios),
        "comentarios": [{"texto": c.texto} for c in planejamento.comentarios]
    }

class AtualizaPlanejamentoSchema(BaseModel):
    encarregado: str  # Este campo é necessário para identificar o planejamento
    equipe: Optional[str] 
    funcao: Optional[str] 
    servico_local: Optional[str] 