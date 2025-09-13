# IADT-F2

Este projeto implementa um sistema de otimização de rotas utilizando algoritmos genéticos para o problema de roteamento de veículos (VRP - Vehicle Routing Problem). O sistema é modular, organizado em pacotes para facilitar a manutenção e extensão.

## Estrutura do Projeto

- **main.py**: Ponto de entrada principal do sistema.
- **api/**: Implementa a interface de comunicação, incluindo suporte a WebSocket.
- **domain/**: Define entidades e regras de negócio, como rotas, soluções e veículos.
- **graph/**: Estruturas de grafos utilizadas para modelar o problema de rotas.
- **genetic_algorithm/**: Implementação dos operadores genéticos (seleção, cruzamento, mutação, etc.) e execução do algoritmo genético.
- **vrp/**: Lógica específica do problema de roteamento de veículos, incluindo construção e ajuste de soluções.

## Como Executar

1. **Pré-requisitos**
   - Docker instalado OU
   - Python 3.13 instalado

2. **Executando com Docker**
   - Construa a imagem:
     ```sh
     docker build -t iadt-f2 .
     ```
   - Execute o container:
     ```sh
     docker run -p 8000:8000 iadt-f2
     ```
   - O sistema será iniciado e estará disponível na porta 8000 (ajuste conforme necessário).

3. **Executando localmente (sem Docker)**
   - Instale as dependências:
     ```sh
     pip install -r requirements.txt
     ```
   - Execute o sistema:
     ```sh
     python main.py
     ```

## Testes

Os testes unitários estão distribuídos nas pastas `test/` dentro de cada módulo. Para rodar todos os testes:

```sh
pytest
```