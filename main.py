# Restrições
# 1 - Prioridade diferente para entregas (medicamentos criticos vs entrega regulares) | 1 ou 0
# 2 - Capacidade do veiculo
# 4 - Multiplos veiculos
# 5 - Equilibrar a distancia percorrida por cada veiculo - ok
# 6 - Custo operacioanal com pedágios

import uvicorn

if __name__ == "__main__":
    uvicorn.run("api.websocket:app", host="0.0.0.0", port=8000, reload=True)
