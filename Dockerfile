# Utiliza uma imagem base oficial do Python 3.13
FROM python:3.13-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia todos os arquivos do projeto para o container
COPY . /app

# Atualiza o pip e instala as dependências do projeto
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Expõe a porta padrão (ajuste se necessário)
EXPOSE 8000

# Comando para iniciar a aplicação principal
CMD ["python", "main.py"]

