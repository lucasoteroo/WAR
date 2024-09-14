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
# Simulando alguns dados
territorios_iniciais = ["Oriente Medio", "Aral", "Omsk", "Dudinka", "Siberia", "Tchita", "Mongolia", "Vladivostok", "China", "India", "Japao", "Vietna", 
                        "Argentina/Uruguai", "Brasil", "Colombia/Venezuela", "Peru/Bolivia/Chile", 
                        "Mexico", "California", "Nova Iorque", "Labrador", "Ottawa", "Vancouver", "Mackenzie", "Alasca", "Groenlandia", 
                        "Alemanha", "Espanha/Portugal/Franca/Italia", "Polonia/Iugoslavia", "Moscou", "Islandia", "Inglaterra", "Suecia", 
                        "Australia", "Borneo", "Sumatra", "Nova Guine",
                        "Argelia/Nigeria", "Egito", "Congo", "Sudao", "Madagascar", "Africa do sul"]

objetivos_possiveis = [
    {"tipo": "conquistar_territorios", "quantidade": 24},
    {"tipo": "controlar_continentes", "continentes": ["Asia", "America do Sul"]},
    {"tipo": "controlar_continentes", "continentes": ["Asia", "Africa"]},
    {"tipo": "controlar_continentes", "continentes": ["America do Norte", "Africa"]},
    {"tipo": "controlar_continentes", "continentes": ["America do Norte", "Oceania"]},
    {"tipo": "eliminar_jogador", "cor": None}
]


continentes = {
    "Asia": ["Oriente Medio", "Aral", "Omsk", "Dudinka", "Siberia", "Tchita", "Mongolia", "Vladivostok", "China", "India", "Japao", "Vietna"],
    "America do Sul": ["Argentina/Uruguai", "Brasil", "Colombia/Venezuela", "Peru/Bolivia/Chile"],
    "America do Norte": ["Mexico", "California", "Nova Iorque", "Labrador", "Ottawa", "Vancouver", "Mackenzie", "Alasca", "Groenlandia"],
    "Europa": ["Alemanha", "Espanha/Portugal/Franca/Italia", "Polonia/Iugoslavia", "Moscou", "Islandia", "Inglaterra", "Suecia"],
    "Africa": ["Argelia/Nigeria", "Egito", "Congo", "Sudao", "Madagascar", "Africa do sul"],
    "Oceania": ["Australia", "Borneo", "Sumatra", "Nova Guine"]
}

adjacencias_territorios= {
    "Oriente Medio": ["Moscou","Aral","Polonia/Iugoslavia", "India", "Egito"],
    "Aral": ["Oriente Medio","Moscou","Omsk", "China", "India"],
    "Omsk": ["Aral","Dudinka","Mongolia", "Moscou", "China"],
    "Dudinka": ["Mongolia","Omsk","Siberia","Tchita"],
    "Siberia": ["Dudinka","Tchita","Vladivostok"],
    "Tchita": ["Dudinka", "China","Vladivostok", "Siberia", "Mongolia"],
    "Mongolia": ["Tchita","Omsk","Dudinka","China"],
    "Vladivostok": ["Tchita","China","Siberia", "Japao", "Alasca"],
    "China": ["Aral","Omsk","Tchita","Mongolia", "Japao", "India", "Vietna", "Vladivostok"],
    "India": ["Oriente Medio","Aral","China","Sumatra", "Vietna"],
    "Japao": ["China", "Vladivostok"],
    "Vietna": ["India","China","Borneo"],
    "Argentina/Uruguai": ["Brasil", "Peru/Bolivia/Chile"],
    "Brasil": ["Argentina/Uruguai", "Colombia/Venezuela", "Peru/Bolivia/Chile", "Argelia/Nigeria"],
    "Colombia/Venezuela": ["Brasil", "Peru/Bolivia/Chile", "Mexico"],
    "Peru/Bolivia/Chile": ["Brasil", "Colombia/Venezuela", "Argentina/Uruguai"],
    "Argelia/Nigeria": ["Brasil", "Espanha/Portugal/Franca/Italia", "Congo","Egito","Sudao"],
    "Egito": ["Argelia/Nigeria", "Espanha/Portugal/Franca/Italia", "Sudao", "Oriente Medio", "Polonia/Iugoslavia"],
    "Congo": ["Africa do sul", "Sudao", "Argelia/Nigeria"],
    "Sudao": ["Africa do sul", "Madagascar", "Argelia/Nigeria", "Egito"],
    "Madagascar": ["Sudao", "Africa do sul"],
    "Africa do Sul": ["Congo", "Sudao", "Madagascar"],
    "Mexico": ["Colombia/Venezuela", "Nova Iorque", "California"],
    "California": ["Mexico", "Ottawa", "Vancouver", "Nova Iorque"],
    "Nova Iorque": ["Labrador", "Ottawa", "California", "Mexico"],
    "Labrador": ["Nova Iorque", "Ottawa", "Groenlandia"],
    "Ottawa": ["California", "Nova Iorque", "Labrador", "Vancouver", "Mackenzie"],
    "Vancouver": ["America do Norte", "Ottawa", "Labrador", "Mackenzie", "Alasca"],
    "Mackenzie": ["Vancouver", "Ottawa", "Alasca", "Groenlandia"],
    "Alasca": ["Vladivostok", "Vancouver", "Mackenzie"],
    "Groenlandia": ["Mackenzie", "Labrador", "Islandia"],
    "Alemanha": ["Inglaterra", "Espanha/Portugal/Franca/Italia", "Polonia/Iugoslavia"],
    "Espanha/Portugal/Franca/Italia": ["Argelia/Nigeria", "Alemanha", "Inglaterra", "Polonia/Iugoslavia", "Egito"],
    "Polonia/Iugoslavia": ["Espanha/Portugal/Franca/Italia", "Alemanha", "Moscou", "Egito", "Oriente Medio"],
    "Moscou": ["Suecia", "Polonia/Iugoslavia", "Oriente Medio", "Aral", "Omsk"],
    "Islandia": ["Inglaterra", "Groenlandia"],
    "Inglaterra": ["Alemanha", "Islandia", "Suecia", "Espanha/Portugal/Franca/Italia"],
    "Suecia": ["Moscou", "Inglaterra"],
    "Australia": ["Nova Guine", "Borneo", "Sumatra"],
    "Borneo": ["Australia", "Vietna", "Nova Guine"],
    "Sumatra": ["Australia", "India"],
    "Nova Guine": ["Australia", "Borneo"]
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

# Função para verificar se um jogador ganhou o jogo
def verificar_vitoria(jogador: Jogador) -> bool:
    objetivo = jogador.objetivo
    
    # Verifica se o jogador completou o objetivo de conquistar territórios
    if objetivo["tipo"] == "conquistar_territorios":
        if len(jogador.territorios) >= objetivo["quantidade"]:
            return True
    
    # Verifica se o jogador controla os continentes necessários
    elif objetivo["tipo"] == "controlar_continentes":
        continentes_controlados = [cont for cont in objetivo["continentes"] if all(territorio in jogador.territorios for territorio in continentes[cont])]
        if len(continentes_controlados) == len(objetivo["continentes"]):
            return True
    
    # Verifica se o jogador eliminou outro jogador
    elif objetivo["tipo"] == "eliminar_jogador":
        jogador_eliminado = all(j.cor_exercito != objetivo["cor"] for j in jogadores)
        if jogador_eliminado:
            return True
    
    return False

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
    
    # Escolhe um objetivo aleatório
    objetivo = random.choice(objetivos_possiveis)
    
    # Se o objetivo for eliminar um jogador, escolhe a cor de um adversário diferente do próprio jogador
    if objetivo["tipo"] == "eliminar_jogador":
        # Filtra os jogadores adversários que possuem uma cor de exército e que não são o próprio jogador
        adversarios = [j for j in jogadores if j.nome != jogador and j.cor_exercito != jogador_obj.cor_exercito]
        
        # Verifica se há adversários disponíveis para evitar erro se todos os jogadores forem eliminados
        if not adversarios:
            raise HTTPException(status_code=400, detail="Nenhum adversário disponível para este objetivo")
        
        # Escolhe a cor do exército de um adversário
        cor_adversario = random.choice(adversarios).cor_exercito
        objetivo["cor"] = cor_adversario  # Atribui a cor do exército do adversário
    
    # Atribui o objetivo ao jogador
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

@app.post("/preparacao/distribuir-exercitos-por-territorio/")
def distribuir_exercitos_por_territorio():
    for jogador in jogadores:
        num_territorios = len(jogador.territorios)
        if num_territorios == 0:
            continue
        
        # Inicialmente, cada território recebe 1 exército
        exército_por_territorio = {territorio: 1 for territorio in jogador.territorios}
        exércitos_restantes = jogador.exercitos - num_territorios  # Sobram os exércitos após colocar 1 em cada território
        
        # Distribuir os exércitos restantes, com limite de 3 exércitos por território
        while exércitos_restantes > 0:
            territorio_aleatorio = random.choice(jogador.territorios)
            
            # Verifica se o território já tem o máximo de 3 exércitos
            if exército_por_territorio[territorio_aleatorio] < 3:
                exército_por_territorio[territorio_aleatorio] += 1
                exércitos_restantes -= 1
        
        # Atualiza os territórios do jogador com o número de exércitos
        jogador.territorios = {territorio: exército_por_territorio[territorio] for territorio in jogador.territorios}
        jogador.exercitos = 0  # Zera os exércitos após distribuição

    return {j.nome: j.territorios for j in jogadores}

@app.post("/rodada/ataque/")
def iniciar_ataque(jogador_atacante: str, territorio_atacante: str, jogador_defensor: str, territorio_defensor: str, mover_exercitos: int = 0):
    atacante = encontrar_jogador(jogador_atacante)
    defensor = encontrar_jogador(jogador_defensor)
    
    # Verifica se o jogador atacante e defensor possuem os territórios mencionados
    if territorio_atacante not in atacante.territorios or territorio_defensor not in defensor.territorios:
        raise HTTPException(status_code=400, detail="Territórios inválidos para ataque")
    
    # Obtém os exércitos de cada território
    exercitos_atacante = atacante.territorios[territorio_atacante]
    exercitos_defensor = defensor.territorios[territorio_defensor]
    
    # Valida se o território atacante tem pelo menos 2 exércitos (1 para ataque e 1 para defesa)
    if exercitos_atacante < 2:
        raise HTTPException(status_code=400, detail="Você precisa de pelo menos 2 exércitos no território atacante")
    
    # Valida se os territórios atacante e defensor são adjacentes (adapte de acordo com as regras)
    if not territorios_sao_adjacentes(territorio_atacante, territorio_defensor):
        raise HTTPException(status_code=400, detail="Territórios não são adjacentes")
    
    # Continua com a rolagem de dados e resolução da batalha
    dados_atacante = rolar_dados(min(3, exercitos_atacante - 1))  # Ataque com até 3 exércitos
    dados_defensor = rolar_dados(min(2, exercitos_defensor))      # Defesa com até 2 exércitos
    
    perdas_atacante = 0
    perdas_defensor = 0
    
    # Comparação dos dados para determinar perdas
    for dado_atacante, dado_defensor in zip(dados_atacante, dados_defensor):
        if dado_atacante > dado_defensor:
            perdas_defensor += 1
        else:
            perdas_atacante += 1
    
    # Atualiza os exércitos no território atacante e defensor
    atacante.territorios[territorio_atacante] -= perdas_atacante
    defensor.territorios[territorio_defensor] -= perdas_defensor
    
    # Se o defensor perde todos os exércitos, atacante conquista o território
    if defensor.territorios[territorio_defensor] <= 0:
        defensor.territorios.pop(territorio_defensor)  # Remove o território do defensor
        
        # Limita a movimentação de exércitos: mínimo de 1 deve permanecer no território original
        exercitos_restantes_no_atacante = atacante.territorios[territorio_atacante]
        if mover_exercitos > exercitos_restantes_no_atacante - 1:
            raise HTTPException(status_code=400, detail=f"Você só pode mover até {exercitos_restantes_no_atacante - 1} exércitos")
        if mover_exercitos < 1:
            raise HTTPException(status_code=400, detail="Você precisa mover pelo menos 1 exército")
        
        # Mover os exércitos escolhidos para o território conquistado
        atacante.territorios[territorio_atacante] -= mover_exercitos
        atacante.territorios[territorio_defensor] = mover_exercitos  # Adiciona o território ao atacante com os exércitos movidos
    
    return {
        "resultados_dados": {
            "atacante": dados_atacante,
            "defensor": dados_defensor
        },
        "resultado_batalha": {
            "atacante": {"nome": atacante.nome, "perdas": perdas_atacante, "exercitos_restantes": atacante.territorios[territorio_atacante]},
            "defensor": {"nome": defensor.nome, "perdas": perdas_defensor, "exercitos_restantes": defensor.territorios.get(territorio_defensor, 0)},
        },
        "conquista": f"{atacante.nome} conquistou {territorio_defensor}" if defensor.territorios.get(territorio_defensor) is None else "Território não conquistado",
        "exercitos_movidos": mover_exercitos if defensor.territorios.get(territorio_defensor) is None else 0
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

@app.get("/verificar-vitoria/")
def verificar_vitoria_geral():
    for jogador in jogadores:
        if verificar_vitoria(jogador):
            return {"message": f"{jogador.nome} venceu o jogo!"}
    return {"message": "Nenhum jogador venceu ainda."}

# Rota para visualizar informações de um jogador
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