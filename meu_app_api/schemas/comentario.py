from pydantic import BaseModel


class ComentarioSchema(BaseModel):
    """ Define como um novo comentário a ser inserido deve ser representado
    """
    planejamento_id: int = 1
    texto: str = "Verificar se a execução está dentro dos padrões."
