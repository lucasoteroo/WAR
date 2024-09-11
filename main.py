from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import random

app = FastAPI()

# Definindo os modelos de dados
class Jogador(BaseModel):
    nome: str
    cor_exercito: str = None
    objetivo: str = None
    territorios: List[str] = []
    exercitos: int = 0
    cartas: List[str] = []

# Simulando alguns dados
territorios_iniciais = ["Território 1", "Território 2", "Território 3", "Território 4", "Território 5"]
objetivos_possiveis = ["Conquistar 24 territórios", "Eliminar um oponente", "Controlar dois continentes"]
cores_disponiveis = ["Vermelho", "Azul", "Verde", "Amarelo"]
cartas_possiveis = ["Carta 1", "Carta 2", "Carta 3"]

jogadores = []

# Preparação
@app.post("/preparacao/escolher-cor/")
def escolher_cor(jogador: str, cor: str):
    for j in jogadores:
        if j.nome == jogador:
            j.cor_exercito = cor
            return {"message": f"O jogador {jogador} escolheu a cor {cor}."}
    return {"error": "Jogador não encontrado"}

@app.post("/preparacao/objetivo/")
def receber_objetivo(jogador: str):
    objetivo = random.choice(objetivos_possiveis)
    for j in jogadores:
        if j.nome == jogador:
            j.objetivo = objetivo
            return {"message": f"Objetivo do jogador {jogador}: {objetivo}"}
    return {"error": "Jogador não encontrado"}

@app.post("/preparacao/definir-ordem/")
def definir_ordem():
    random.shuffle(jogadores)
    ordem = [j.nome for j in jogadores]
    return {"ordem": ordem}

@app.post("/preparacao/distribuir-territorios/")
def distribuir_territorios():
    random.shuffle(territorios_iniciais)
    for i, jogador in enumerate(jogadores):
        jogador.territorios.append(territorios_iniciais[i % len(jogadores)])
    return {j.nome: j.territorios for j in jogadores}

@app.post("/preparacao/distribuir-exercitos/")
def distribuir_exercitos(jogador: str, exercitos: int):
    for j in jogadores:
        if j.nome == jogador:
            j.exercitos += exercitos
            return {"message": f"{exercitos} exércitos distribuídos para o jogador {jogador}"}
    return {"error": "Jogador não encontrado"}

# Rodada
@app.post("/rodada/iniciar/")
def iniciar_rodada():
    for j in jogadores:
        j.exercitos += 5  # Supondo 5 exércitos por rodada
    return {j.nome: j.exercitos for j in jogadores}

@app.post("/rodada/ataque/")
def iniciar_ataque(jogador_atacante: str, jogador_defensor: str, territorios: List[str]):
    return {"message": f"{jogador_atacante} iniciou um ataque a {jogador_defensor} nos territórios {territorios}"}

@app.post("/rodada/receber-cartas/")
def receber_cartas(jogador: str):
    carta = random.choice(cartas_possiveis)
    for j in jogadores:
        if j.nome == jogador:
            j.cartas.append(carta)
            return {"message": f"O jogador {jogador} recebeu a carta {carta}"}
    return {"error": "Jogador não encontrado"}

@app.post("/rodada/mover-exercitos/")
def mover_exercitos(jogador: str, origem: str, destino: str, quantidade: int):
    return {"message": f"{jogador} moveu {quantidade} exércitos de {origem} para {destino}"}

@app.post("/rodada/troca-cartas/")
def trocar_cartas(jogador: str, cartas: List[str]):
    return {"message": f"{jogador} trocou as cartas {cartas}"}

@app.get("/objetivo/verificar/")
def verificar_objetivo(jogador: str):
    for j in jogadores:
        if j.nome == jogador:
            # Verificação fictícia
            return {"message": f"O jogador {jogador} não completou o objetivo ainda"}
    return {"error": "Jogador não encontrado"}

# Endpoint para adicionar jogadores
@app.post("/jogadores/adicionar/")
def adicionar_jogador(nome: str):
    jogador = Jogador(nome=nome)
    jogadores.append(jogador)
    return {"message": f"Jogador {jogador.nome} adicionado com sucesso"}

# Rota padrão da FastAPI para acessar a documentação
