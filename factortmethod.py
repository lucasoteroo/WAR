from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import List, Dict

class Jogador(BaseModel):
    nome: str
    cor_exercito: str = None
    objetivo: str = None
    territorios: Dict[str, int] = []
    exercitos: int = 0
    cartas: List[str] = []
    
class CriadorDeJogador(ABC):
    @abstractmethod
    def criar_jogador(self, nome: str) -> Jogador:
        pass

class CriadorJogador(CriadorDeJogador):
    def criar_jogador(self, nome: str) -> Jogador:
        return Jogador(nome=nome)
