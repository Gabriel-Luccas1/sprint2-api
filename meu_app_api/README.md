## Apresentação do Projeto

Meu projeto consiste em um planejamento semanal de obra, envolvendo a definição das tarefas a serem executadas, as equipes responsáveis e os respectivos encarregados.

## Detalhes dos Itens

Os itens inseridos no planejamento incluem:
- Nome do encarregado
- Equipe designada
- Função da equipe (pedreiro, ladrilheiro, bombeiro, etc.)
- Descrição do serviço a ser executado
- Local a serem executados

## Objetivo do Projeto

O objetivo principal é facilitar a organização e gestão das atividades, proporcionando um registro estruturado das informações cruciais para o andamento eficiente das obras.



## Como executar


Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.
Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

```
(env)$ pip install -r requirements.txt
```

Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

Para executar a API  basta executar:

```flask run --host 0.0.0.0 --port 5000
(env)$ flask run --host 0.0.0.0 --port 5000
```

Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução.
