from pathlib import Path
from typing import List

import pandas as pd

from app.config import EMPLOYEES_CSV
from app.models.funcionario import Funcionario
from app.models.turno import Turno


class EmployeeCSVRepository:
    def __init__(self, path: Path | str = EMPLOYEES_CSV):
        self.path = Path(path)

    def load_all(self) -> List[Funcionario]:
        """
        Lê todos os funcionários do CSV.
        Se o arquivo não existir, retorna lista vazia.
        """
        if not self.path.exists():
            return []

        df = pd.read_csv(self.path, dtype={"matricula": str})
        funcionarios: List[Funcionario] = []

        for _, row in df.iterrows():
            funcionarios.append(
                Funcionario(
                    matricula=str(row["matricula"]),
                    nome=str(row["nome"]),
                    idade=int(row["idade"]),
                    turno=Turno(row["turno"]),  # converte texto -> Enum
                )
            )

        return funcionarios

    def save_all(self, funcionarios: List[Funcionario]) -> None:
        """
        Sobrescreve o CSV com a lista de funcionários atual.
        """
        self.path.parent.mkdir(parents=True, exist_ok=True)
        df = pd.DataFrame([f.to_dict() for f in funcionarios])
        df.to_csv(self.path, index=False)
