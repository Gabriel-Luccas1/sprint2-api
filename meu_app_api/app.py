from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, Flask, jsonify
from urllib.parse import unquote
import requests
from model import Session, Planejamento, Comentario
from logger import logger
from schemas import *
from flask_cors import CORS

from schemas.planejamento import apresenta_planejamento

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
planejamento_tag = Tag(name="Planejamento", description="Adição, visualização e remoção de planejamentos à base")
comentario_tag = Tag(name="Comentario", description="Adição de um comentário à um planejamentos cadastrado na base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/planejamento_add', tags=[planejamento_tag],
          responses={"200": PlanejamentoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_planejamento(form: PlanejamentoSchema):
    """Adiciona um novo Planejamento à base de dados

    Retorna uma representação dos planejamentos e comentários associados.
    """
    planejamento = Planejamento(
        encarregado=form.encarregado,
        equipe=form.equipe,
        funcao=form.funcao,
        servico_local=form.servico_local )
    logger.debug(f"Adicionando planejamento de nome: '{planejamento.encarregado}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando planejamento
        session.add(planejamento)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado planejamento de nome: '{planejamento.encarregado}'")
        return apresenta_planejamento(planejamento), 200

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar planejamento '{planejamento.encarregado}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.get('/planejamento', tags=[planejamento_tag],
         responses={"200": ListagemPlanejamentosSchema, "404": ErrorSchema})
def get_planejamentos():
    """Faz a busca por todos os Planejamento cadastrados

    Retorna uma representação da listagem de planejamento.
    """
    logger.debug(f"Coletando planejamentos ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    planejamentos = session.query(Planejamento).all()

    if not planejamentos:
        # se não há planejamentos cadastrados
        return {"planejamentos": []}, 200
    else:
        logger.debug(f"%d planejamentos econtrados" % len(planejamentos))
        # retorna a representação de planejamento
        print(planejamentos)
        return apresenta_planejamentos(planejamentos), 200




@app.delete('/planejamento', tags=[planejamento_tag],
            responses={"200": PlanejamentoDelSchema, "404": ErrorSchema})
def del_planejamento(query: PlanejamentoBuscaSchema):
    """Deleta um Planejamento a partir do nome de planejamento informado

    Retorna uma mensagem de confirmação da remoção.
    """
    planejamento_encarregado = unquote(unquote(query.encarregado))
    print(planejamento_encarregado)
    logger.debug(f"Deletando dados sobre planejamento #{planejamento_encarregado}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Planejamento).filter(Planejamento.encarregado == planejamento_encarregado).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado planejamento #{planejamento_encarregado}")
        return {"mesage": "Planejamento removido", "id": planejamento_encarregado}
    else:
        # se o planejamento não foi encontrado
        error_msg = "planejamento não encontrado na base :/"
        logger.warning(f"Erro ao deletar planejamento #'{planejamento_encarregado}', {error_msg}")
        return {"mesage": error_msg}, 404
    
@app.post('/comentario', tags=[comentario_tag],
          responses={"200": PlanejamentoViewSchema, "404": ErrorSchema})
def add_comentario(form: ComentarioSchema):
    """Adiciona de um novo comentário à um planejamentos cadastrado na base identificado pelo id

    Retorna uma representação dos planejamentos e comentários associados.
    """
    planejamento_id  = form.planejamento_id
    logger.debug(f"Adicionando comentários ao planejamento #{planejamento_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca pelo planejamento
    planejamento = session.query(Planejamento).filter(Planejamento.id == planejamento_id).first()

    if not planejamento:
        # se planejamento não encontrado
        error_msg = "Planejamento não encontrado na base :/"
        logger.warning(f"Erro ao adicionar comentário ao planejamento '{planejamento_id}', {error_msg}")
        return {"message": error_msg}, 404

    # criando o comentário
    texto = form.texto
    comentario = Comentario(texto)

    # adicionando o comentário ao planejamento
    planejamento.adiciona_comentario(comentario)
    session.commit()

    logger.debug(f"Adicionado comentário ao planejamento #{planejamento_id}")

    # retorna a representação de planejamento
    return apresenta_planejamento(planejamento), 200

@app.put('/planejamento/<encarregado>', tags=[planejamento_tag],
        responses={"200": PlanejamentoViewSchema, "404": ErrorSchema, "400": ErrorSchema})
def update_planejamento(form: AtualizaPlanejamentoSchema):
    """Atualiza um Planejamento com base no encarregado

    Retorna uma representação do planejamento atualizado.
    """
    encarregado = unquote(unquote(form.encarregado))
    logger.debug(f"Atualizando planejamento para o encarregado: '{encarregado}'")

    session = Session()
    planejamento = session.query(Planejamento).filter(Planejamento.encarregado == encarregado).first()

    if not planejamento:
        error_msg = "Planejamento não encontrado na base :/"
        logger.warning(f"Erro ao atualizar planejamento '{encarregado}', {error_msg}")
        return {"message": error_msg}, 404

    # Atualiza apenas os campos fornecidos
    if form.equipe:
        planejamento.equipe = form.equipe
    if form.funcao:
        planejamento.funcao = form.funcao
    if form.servico_local:
        planejamento.servico_local = form.servico_local

    # Confirma a atualização
    session.commit()

    logger.debug(f"Planejamento atualizado para o encarregado: '{encarregado}'")

    # Retorna a representação do planejamento atualizado
    return apresenta_planejamento(planejamento), 200

