# Use uma imagem base do Python para Flask
FROM python:3.9-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie os arquivos de código-fonte para o diretório de trabalho do contêiner
COPY . .

# Instale as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta em que a API estará acessível
EXPOSE 5000

# Comando para iniciar o servidor Flask e executar a API
CMD ["flask", "run", "--host=0.0.0.0"]
