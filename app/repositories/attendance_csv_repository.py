from pathlib import Path
from typing import List

import pandas as pd

from app.config import ATTENDANCE_CSV
from app.models.registro_ponto import RegistroPonto


class AttendanceCSVRepository:
    def __init__(self, path: Path | str = ATTENDANCE_CSV):
        self.path = Path(path)

    def load_all(self) -> List[RegistroPonto]:
        """
        Lê todos os registros do CSV.
        """
        if not self.path.exists():
            return []

        df = pd.read_csv(self.path, dtype={"matricula": str, "tipo": str})
        if "timestamp" in df.columns:
            df["timestamp"] = pd.to_datetime(df["timestamp"])

        registros: List[RegistroPonto] = []
        for _, row in df.iterrows():
            registros.append(
                RegistroPonto(
                    matricula=str(row["matricula"]),
                    timestamp=row["timestamp"],
                    tipo=str(row["tipo"]),
                )
            )

        return registros

    def append(self, registro: RegistroPonto) -> None:
        """
        Acrescenta um novo registro no CSV (modo append).
        """
        self.path.parent.mkdir(parents=True, exist_ok=True)
        df = pd.DataFrame([registro.to_dict()])
        header = not self.path.exists()
        df.to_csv(self.path, mode="a", header=header, index=False)
