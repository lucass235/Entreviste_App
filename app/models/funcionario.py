from dataclasses import dataclass, asdict
from typing import Dict

from .turno import Turno


@dataclass
class Funcionario:
    """
    Representa um funcionário da empresa.
    """
    matricula: str
    nome: str
    idade: int
    turno: Turno

    def to_dict(self) -> Dict:
        """
        Converte para dicionário compatível com DataFrame/CSV.
        """
        d = asdict(self)
        d["turno"] = self.turno.value  # salva texto legível
        return d
