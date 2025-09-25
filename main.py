# Restrições
#
# 1 - Prioridade diferente para entregas (medicamentos criticos vs entrega regulares) | 1 ou 0 - ok
# 2 - Capacidade do veiculo - ok
# 3 - Autonomia (distancia máxima percorrida) - nok
# 4 - Multiplos veiculos - ok

# Restrições extras implementadas
# Equilibrar a distancia percorrida por cada veiculo - ok

# Restrições extras (opcionais)
# Custos operacionais (pedágios) - Maybe - Definir 1 pedagio a cada 50km, pune a cada pedagio presente no trajeto entre dois pontos - ok
# Restrições de rota (ex: evitar certas ruas, zonas de baixa emissão) - Maybe

# Ideias
# Visualização do mapa com rotas reais
# Diferentes tipos de veiculos (motos, carros, caminhões)
# Diferentes capacidades e custos dos veiculos
# Usar cidadades reais
# Analisar o melhor veiculo para entregar a carga (ex: motos para entregas pequenas e rápidas, caminhões para cargas maiores)
# Centro de distribuição, a carga vai até o centro e depois é distribuida pelos veiculos menores
# Informar o tempo estimado de entrega
# Usuário parametrizar o problema (número de veiculos, capacidade, etc)
# Interface web
# Separar o código em frontend e backend

import uvicorn

if __name__ == "__main__":
    uvicorn.run("api.websocket:app", host="0.0.0.0", port=8000, reload=True)
