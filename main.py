from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import random

app = FastAPI()

# Definindo os modelos de dados
class Jogador(BaseModel):
    nome: str
    cor_exercito: str = None
    objetivo: str = None
    territorios: Dict[str, int] = []
    exercitos: int = 0
    cartas: List[str] = []

# Simulando alguns dados
territorios_iniciais = ["Oriente Médio", "Aral", "Omsk", "Dudinka", "Sibéria", "Tchita", "Mongólia", "Vladivostok", "China", "Índia", "Japão", "Vietnã", 
                        "Argentina/Uruguai", "Brasil", "Colômbia/Venezuela", "Peru/Bolívia/Chile", 
                        "Mexico", "California", "Nova Iorque", "Labrador", "Ottawa", "Vancouver", "Mackenzie", "Alasca", "Groenlândia", 
                        "Alemanha", "Espanha/Portugal/França/Itália", "Polônia/Iugoslávia", "Moscou", "Islândia", "Inglaterra", "Suécia", 
                        "Australia", "Bornéu", "Sumatra", "Nova Guiné",
                        "Argélia/Nigéria", "Egito", "Congo", "Sudão", "Madagascar", "Africa do sul"]

objetivos_possiveis = [
    {"tipo": "conquistar_territorios", "quantidade": 24},
    {"tipo": "controlar_continentes", "continentes": ["Ásia", "América do Sul"]},
    {"tipo": "eliminar_jogador", "cor": None}
]

continentes = {
    "Ásia": ["Oriente Médio", "Aral", "Omsk", "Dudinka", "Sibéria", "Tchita", "Mongólia", "Vladivostok", "China", "Índia", "Japão", "Vietnã"],
    "América do Sul": ["Argentina/Uruguai", "Brasil", "Colômbia/Venezuela", "Peru/Bolívia/Chile"],
    "America do Norte": ["Mexico", "California", "Nova Iorque", "Labrador", "Ottawa", "Vancouver", "Mackenzie", "Alasca", "Groenlândia"],
    "Europa": ["Alemanha", "Espanha/Portugal/França/Itália", "Polônia/Iugoslávia", "Moscou", "Islândia", "Inglaterra", "Suécia"],
    "Africa": ["Argélia/Nigéria", "Egito", "Congo", "Sudão", "Madagascar", "Africa do sul"],
    "Oceania": ["Australia", "Bornéu", "Sumatra", "Nova Guiné"]
}

adjacencias_territorios= {
    "Oriente Médio": ["Moscou","Aral","Polônia/Iugoslávia", "Índia", "Egito"],
    "Aral": ["Oriente Médio","Moscou","Omsk", "China", "Índia"],
    "Omsk": ["Aral","Dudinka","Mongólia", "Moscou", "China"],
    "Dudinka": ["Mongólia","Omsk","Sibéria","Tchita"],
    "Sibéria": ["Dudinka","Tchita","Vladivostok"],
    "Tchita": ["Dudinka", "China","Vladivostok", "Sibéria", "Mongólia"],
    "Mongólia": ["Tchita","Omsk","Dudinka","China"],
    "Vladivostok": ["Tchita","China","Sibéria", "Japão", "Alasca"],
    "China": ["Aral","Omsk","Tchita","Mongólia", "Japão", "Índia", "Vietnã", "Vladivostok"],
    "Índia": ["Oriente Médio","Aral","China","Sumatra", "Vietnã"],
    "Japão": ["China", "Vladivostok"],
    "Vietnã": ["Índia","China","Bornéu"],
    "Argentina/Uruguai": ["Brasil", "Peru/Bolivia/Chile"],
    "Brasil": ["Argentina/Uruguai", "Colômbia/Venezuela", "Peru/Bolivia/Chile", "Argélia/Nigéria"],
    "Colômbia/Venezuela": ["Brasil", "Peru/Bolívia/Chile", "México"],
    "Peru/Bolívia/Chile": ["Brasil", "Colômbia/Venezuela", "Argentina/Uruguai"],
    "Argélia/Nigéria": ["Brasil", "Espanha/Portugal/França/Itália", "Congo","Egito","Sudão"],
    "Egito": ["Argélia/Nigéria", "Espanha/Portugal/França/Itália", "Sudão", "Oriente Médio", "Polônia/Iugoslávia"],
    "Congo": ["Africa do sul", "Sudão", "Argélia/Nigéria"],
    "Sudão": ["Africa do sul", "Madagascar", "Argélia/Nigéria", "Egito"],
    "Madagascar": ["Sudão", "Africa do sul"],
    "Africa do Sul": ["Congo", "Sudão", "Madagascar"],
    "México": ["Colômbia/Venezuela", "Nova Iorque", "Califónia"],
    "California": ["México", "Ottawa", "Vancouver", "Nova Iorque"],
    "Nova Iorque": ["Labrador", "Ottawa", "California", "México"],
    "Labrador": ["Nova Iorque", "Ottawa", "Groenlândia"],
    "Ottawa": ["California", "Nova Iorque", "Labrador", "Vancouver", "Mackenzie"],
    "Vancouver": ["America do Norte", "Ottawa", "Labrador", "Mackenzie", "Alasca"],
    "Mackenzie": ["Vancouver", "Ottawa", "Alasca", "Groenlândia"],
    "Alasca": ["Vladivostok", "Vancouver", "Mackenzie"],
    "Groenlândia": ["Mackenzie", "Labrador", "Islândia"],
    "Alemanha": ["Inglaterra", "Espanha/Portugal/França/Itália", "Polônia/Iugoslávia"],
    "Espanha/Portugal/França/Itália": ["Argélia/Nigéria", "Alemanha", "Inglaterra", "Polônia/Iugoslávia", "Egito"],
    "Polônia/Iugoslávia": ["Espanha/Portugal/França/Itália", "Alemanha", "Moscou", "Egito", "Oriente Médio"],
    "Moscou": ["Suécia", "Polônia/Iugoslávia", "Oriente Médio", "Aral", "Omsk"],
    "Islândia": ["Inglaterra", "Groenlândia"],
    "Inglaterra": ["Alemanha", "Islândia", "Suécia", "Espanha/Portugal/França/Itália"],
    "Suécia": ["Moscou", "Inglaterra"],
    "Australia": ["Nova Guiné", "Bornéu", "Sumatra"],
    "Bornéu": ["Australia", "Vietnâ", "Nova Guiné"],
    "Sumatra": ["Australia", "Índia"],
    "Nova Guiné": ["Australia", "Bornéu"]
    
}

cores_disponiveis = ["Vermelho", "Azul", "Verde", "Amarelo", "Branco", "Preto"]
cartas_possiveis = ["Quadrado", "Triangulo", "Circulo"]

jogadores = []
ordem_jogadores = []
trocas_de_cartas = 0  # Contador global de trocas



# Função auxiliar para encontrar jogador
def encontrar_jogador(nome: str) -> Jogador:
    for j in jogadores:
        if j.nome == nome:
            return j
    raise HTTPException(status_code=404, detail="Jogador não encontrado")

# Função auxiliar para rolar dados
def rolar_dados(quantidade: int) -> List[int]:
    return sorted([random.randint(1, 6) for _ in range(quantidade)], reverse=True)

# Função para verificar se dois territórios são adjacentes
def territorios_sao_adjacentes(territorio1: str, territorio2: str) -> bool:
    return territorio2 in adjacencias_territorios.get(territorio1, [])

# Função para bônus de exércitos por continente controlado
def controlar_continente(jogador: Jogador) -> int:
    exercitos_bonus = 0
    for continente, territorios in continentes.items():
        if all(territorio in jogador.territorios for territorio in territorios):
            if continente == "Ásia":
                exercitos_bonus += 7
            elif continente == "América do Norte":
                exercitos_bonus += 5
            elif continente == "Europa":
                exercitos_bonus += 5
            elif continente == "África":
                exercitos_bonus += 3
            elif continente == "Oceania":
                exercitos_bonus += 2
            elif continente == "América do Sul":
                exercitos_bonus += 2
    return exercitos_bonus

@app.post("/jogadores/adicionar/")
def adicionar_jogador(nome: str):
    if any(j.nome == nome for j in jogadores):
        raise HTTPException(status_code=400, detail="Jogador já existe")
    jogador = Jogador(nome=nome)
    jogadores.append(jogador)
    return {"message": f"Jogador {jogador.nome} adicionado com sucesso"}

@app.post("/preparacao/escolher-cor/")
def escolher_cor(jogador: str, cor: str):
    if cor not in cores_disponiveis:
        return {"error": "Cor não disponível"}
    jogador_obj = encontrar_jogador(jogador)
    jogador_obj.cor_exercito = cor
    cores_disponiveis.remove(cor)
    return {"message": f"O jogador {jogador} escolheu a cor {cor}."}

@app.post("/preparacao/objetivo/")
def receber_objetivo(jogador: str):
    jogador_obj = encontrar_jogador(jogador)
    
    objetivo = random.choice(objetivos_possiveis)
    
    # Se o objetivo for eliminar um jogador, escolhe a cor de um adversário
    if objetivo["tipo"] == "eliminar_jogador":
        adversarios = [j for j in jogadores if j.nome != jogador and j.cor_exercito]
        cor_adversario = random.choice(adversarios).cor_exercito
        objetivo["cor"] = cor_adversario  # Atribui a cor do exército do adversário
        
    jogador_obj.objetivo = objetivo
    return {"message": f"Objetivo do jogador {jogador}: {objetivo}"}


@app.post("/preparacao/definir-ordem/")
def definir_ordem():
    global ordem_jogadores
    random.shuffle(jogadores)
    ordem_jogadores = [j.nome for j in jogadores]
    return {"ordem": ordem_jogadores}

@app.post("/preparacao/distribuir-territorios/")
def distribuir_territorios():
    if not jogadores:
        raise HTTPException(status_code=400, detail="Nenhum jogador adicionado")
    
    if not ordem_jogadores:
        raise HTTPException(status_code=400, detail="A ordem dos turnos não foi definida")

    random.shuffle(territorios_iniciais)  # Embaralha os territórios para distribuição aleatória
    numero_jogadores = len(jogadores)
    numero_territorios = len(territorios_iniciais)
    territ_por_jogador = numero_territorios // numero_jogadores  # Quantidade mínima de territórios por jogador
    territ_restantes = numero_territorios % numero_jogadores      # Territórios "extras" que serão distribuídos conforme a ordem

    # Mapeia a ordem dos nomes de jogadores para os objetos Jogador
    jogadores_ordenados = [encontrar_jogador(nome) for nome in ordem_jogadores]

    # Limpa os territórios de todos os jogadores antes da nova distribuição
    for jogador in jogadores_ordenados:
        jogador.territorios = []

    # Distribuição inicial (igual para todos)
    for i in range(territ_por_jogador):
        for j in jogadores_ordenados:
            territorio_atual = territorios_iniciais.pop(0)
            j.territorios.append(territorio_atual)

    # Distribui territórios restantes conforme a ordem de turnos
    for i in range(territ_restantes):
        territorio_atual = territorios_iniciais.pop(0)
        jogadores_ordenados[i].territorios.append(territorio_atual)

    return {j.nome: j.territorios for j in jogadores_ordenados}

@app.post("/preparacao/distribuir-exercitos/")
def distribuir_exercitos(jogador: str, exercitos: int):
    jogador_obj = encontrar_jogador(jogador)
    jogador_obj.exercitos += exercitos
    return {"message": f"{exercitos} exércitos distribuídos para o jogador {jogador}"}

@app.post("/preparacao/distribuir-exercitos-iniciais/")
def distribuir_exercitos_iniciais():
    numero_jogadores = len(jogadores)
    if numero_jogadores == 6:
        exercitos_por_jogador = 20
    elif numero_jogadores == 5:
        exercitos_por_jogador = 25
    elif numero_jogadores == 4:
        exercitos_por_jogador = 30
    elif numero_jogadores == 3:
        exercitos_por_jogador = 35
    elif numero_jogadores == 2:
        exercitos_por_jogador = 40
    else:
        raise HTTPException(status_code=400, detail="Número de jogadores inválido.")

    for jogador in jogadores:
        jogador.exercitos += exercitos_por_jogador
    
    return {"message": f"Exércitos iniciais distribuídos. Cada jogador recebeu {exercitos_por_jogador} exércitos."}

# Rodada
@app.post("/rodada/iniciar/") 
def iniciar_rodada():
    for j in jogadores:
        j.exercitos += 5  # Supondo 5 exércitos por rodada
    return {j.nome: j.exercitos for j in jogadores}

@app.post("/rodada/ataque/")
def iniciar_ataque(jogador_atacante: str, territorio_atacante: str, jogador_defensor: str, territorio_defensor: str):
    atacante = encontrar_jogador(jogador_atacante)
    defensor = encontrar_jogador(jogador_defensor)
    
    # Verifica se o jogador atacante e defensor possuem os territórios mencionados
    if territorio_atacante not in atacante.territorios or territorio_defensor not in defensor.territorios:
        raise HTTPException(status_code=400, detail="Territórios inválidos para ataque")
    
    # Valida se o território atacante tem mais de 1 exército
    if atacante.exercitos < 2:
        raise HTTPException(status_code=400, detail="Exércitos insuficientes para atacar")
    
    # Valida se os territórios atacante e defensor são adjacentes (adapte de acordo com as regras)
    # Aqui deve-se implementar uma lógica para verificar a conexão dos territórios, como uma lista de adjacências
    # Exemplo:
    if not territorios_sao_adjacentes(territorio_atacante, territorio_defensor):
        raise HTTPException(status_code=400, detail="Territórios não são adjacentes")
    
    # Continua com a rolagem de dados e resolução da batalha
    dados_atacante = rolar_dados(min(3, atacante.exercitos - 1))  # Ataque com até 3 exércitos
    dados_defensor = rolar_dados(min(2, defensor.exercitos))      # Defesa com até 2 exércitos
    
    perdas_atacante = 0
    perdas_defensor = 0
    
    # Comparação dos dados para determinar perdas
    for dado_atacante, dado_defensor in zip(dados_atacante, dados_defensor):
        if dado_atacante > dado_defensor:
            perdas_defensor += 1
        else:
            perdas_atacante += 1
    
    atacante.exercitos -= perdas_atacante
    defensor.exercitos -= perdas_defensor
    
    # Se o defensor perde todos os exércitos, atacante conquista o território
    if defensor.exercitos <= 0:
        defensor.territorios.remove(territorio_defensor)
        atacante.territorios.append(territorio_defensor)
    
    return {
        "resultados_dados": {
            "atacante": dados_atacante,
            "defensor": dados_defensor
        },
        "resultado_batalha": {
            "atacante": {"nome": atacante.nome, "perdas": perdas_atacante, "exercitos_restantes": atacante.exercitos},
            "defensor": {"nome": defensor.nome, "perdas": perdas_defensor, "exercitos_restantes": defensor.exercitos},
        },
        "conquista": f"{atacante.nome} conquistou {territorio_defensor}" if defensor.exercitos <= 0 else "Território não conquistado"
    }


@app.post("/rodada/receber-cartas/")
def receber_cartas(jogador: str):
    jogador_obj = encontrar_jogador(jogador)
    carta = random.choice(cartas_possiveis)
    jogador_obj.cartas.append(carta)
    return {"message": f"O jogador {jogador} recebeu a carta {carta}"}

@app.post("/rodada/mover-exercitos/")
def mover_exercitos(jogador: str, origem: str, destino: str, quantidade: int):
    jogador_obj = encontrar_jogador(jogador)

    # Verifica se ambos os territórios pertencem ao jogador
    if origem not in jogador_obj.territorios or destino not in jogador_obj.territorios:
        raise HTTPException(status_code=400, detail="Movimento inválido: territórios não pertencem ao jogador.")
    
    # Verifica se os territórios são adjacentes (adicione lógica para validar isso)
    if not territorios_sao_adjacentes(origem, destino):
        raise HTTPException(status_code=400, detail="Movimento inválido: os territórios não são adjacentes.")
    
    # Verifica se o território de origem tem exércitos suficientes
    if jogador_obj.territorios[origem] < quantidade or quantidade <= 0:
        raise HTTPException(status_code=400, detail=f"Movimento inválido: não há exércitos suficientes em {origem}.")
    
    # Movimenta os exércitos
    jogador_obj.territorios[origem] -= quantidade
    jogador_obj.territorios[destino] += quantidade

    return {"message": f"{quantidade} exércitos movidos de {origem} para {destino} pelo jogador {jogador}."}



@app.post("/rodada/trocar-cartas/")
def trocar_cartas(jogador: str, cartas: List[str]):
    jogador_obj = encontrar_jogador(jogador)

    if len(cartas) != 3:
        raise HTTPException(status_code=400, detail="São necessárias 3 cartas para trocar por exércitos.")
    
    # Verifica se o jogador tem as cartas
    for carta in cartas:
        if carta not in jogador_obj.cartas:
            raise HTTPException(status_code=400, detail="Jogador não tem as cartas especificadas.")

    # Verifica se as cartas formam uma combinação válida (todos iguais ou uma de cada tipo)
    if len(set(cartas)) == 1 or len(set(cartas)) == 3:
        # Remove as cartas do jogador
        for carta in cartas:
            jogador_obj.cartas.remove(carta)

        global trocas_de_cartas
        trocas_de_cartas += 1
        exercitos_ganhos = 4 + (trocas_de_cartas - 1) * 2  # Primeira troca dá 4 exércitos, depois aumenta em 2 cada vez
        jogador_obj.exercitos += exercitos_ganhos

        return {"message": f"Troca bem-sucedida! {jogador} recebeu {exercitos_ganhos} exércitos."}
    
    raise HTTPException(status_code=400, detail="Cartas inválidas para troca.")


@app.post("/rodada/exercitos-por-continente/")
def exercitos_bonus_por_continente():
    for jogador in jogadores:
        exercitos_bonus = controlar_continente(jogador)
        jogador.exercitos += exercitos_bonus
    return {j.nome: j.exercitos for j in jogadores}

@app.get("/objetivo/verificar/")
def verificar_objetivo(jogador: str):
    jogador_obj = encontrar_jogador(jogador)
    objetivo = jogador_obj.objetivo
    
    # Verificação para "conquistar_territorios"
    if objetivo["tipo"] == "conquistar_territorios":
        if len(jogador_obj.territorios) >= objetivo["quantidade"]:
            return {"message": f"O jogador {jogador} atingiu o objetivo de conquistar {objetivo['quantidade']} territórios!"}
    
    # Verificação para "controlar_continentes"
    elif objetivo["tipo"] == "controlar_continentes":
        continentes_conquistados = []
        for continente, territorios in continentes.items():
            if all(territorio in jogador_obj.territorios for territorio in territorios):
                continentes_conquistados.append(continente)
        if set(objetivo["continentes"]).issubset(continentes_conquistados):
            return {"message": f"O jogador {jogador} atingiu o objetivo de controlar os continentes: {', '.join(objetivo['continentes'])}!"}
    
    # Verificação para "eliminar_jogador" por cor do exército
    elif objetivo["tipo"] == "eliminar_jogador":
        cor_adversario = objetivo["cor"]
        try:
            jogador_adversario = next(j for j in jogadores if j.cor_exercito == cor_adversario)
            if not jogador_adversario.territorios:  # Se o jogador foi eliminado (sem territórios)
                return {"message": f"O jogador {jogador} atingiu o objetivo de eliminar o jogador com a cor {cor_adversario}!"}
        except StopIteration:
            return {"message": f"O jogador {jogador} atingiu o objetivo de eliminar o jogador com a cor {cor_adversario}!"}

    return {"message": f"O jogador {jogador} ainda não completou o objetivo"}


# Nova rota para visualizar informações de um jogador
@app.get("/jogadores/ver/")
def ver_jogador(nome: str):
    jogador = encontrar_jogador(nome)
    return {
        "nome": jogador.nome,
        "cor_exercito": jogador.cor_exercito,
        "objetivo": jogador.objetivo,
        "territorios": jogador.territorios,
        "exercitos": jogador.exercitos,
        "cartas": jogador.cartas
    }