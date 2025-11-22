from dataclasses import dataclass
from datetime import datetime
from typing import Dict


@dataclass
class RegistroPonto:
    """
    Um evento de ponto: entrada ou saída em um instante.
    """
    matricula: str
    timestamp: datetime
    tipo: str  # "entrada" ou "saida"

    def to_dict(self) -> Dict:
        """
        Converte para dicionário compatível com DataFrame/CSV.
        """
        return {
            "matricula": self.matricula,
            # Formato "YYYY-MM-DD HH:MM:SS.ffffff" (igual ao seu CSV)
            "timestamp": self.timestamp.isoformat(sep=" "),
            "tipo": self.tipo,
        }
