from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

import matplotlib.pyplot as plt
import pandas as pd

from app.config import GRAFICO_IDADE, GRAFICO_TURNO
from app.models.funcionario import Funcionario
from app.models.turno import Turno
from app.models.registro_ponto import RegistroPonto
from app.repositories.employee_csv_repository import EmployeeCSVRepository
from app.repositories.attendance_csv_repository import AttendanceCSVRepository


class SistemaPonto:
    """
    Regras de negócio do sistema de ponto.

    - cadastra funcionários
    - registra entrada/saída
    - gera DataFrames
    - gera gráficos (barras + pizza)
    - conversa com os repositórios CSV
    """

    def __init__(
        self,
        employee_repo: Optional[EmployeeCSVRepository] = None,
        attendance_repo: Optional[AttendanceCSVRepository] = None,
    ) -> None:
        self.employee_repo = employee_repo or EmployeeCSVRepository()
        self.attendance_repo = attendance_repo or AttendanceCSVRepository()

        # Carrega dados dos CSVs
        self._funcionarios: Dict[str, Funcionario] = {
            f.matricula: f for f in self.employee_repo.load_all()
        }
        self._registros: List[RegistroPonto] = self.attendance_repo.load_all()

    # ---------- FUNCIONÁRIOS ----------

    def cadastrar_funcionario(self, matricula: str, nome: str, idade: int, turno: str) -> None:
        """
        Cadastra um novo funcionário.

        turno deve ser: MATUTINO, VESPERTINO ou NOTURNO (case-insensitive).
        """
        matricula = str(matricula)

        if matricula in self._funcionarios:
            raise ValueError(f"Já existe funcionário com matrícula {matricula}.")

        try:
            turno_enum = Turno[turno.upper()]
        except KeyError:
            raise ValueError("Turno inválido. Use: MATUTINO, VESPERTINO ou NOTURNO.")

        funcionario = Funcionario(
            matricula=matricula,
            nome=nome,
            idade=int(idade),
            turno=turno_enum,
        )

        self._funcionarios[matricula] = funcionario

        # Persiste imediatamente no CSV
        self.employee_repo.save_all(self.listar_funcionarios())

    def listar_funcionarios(self) -> List[Funcionario]:
        return list(self._funcionarios.values())

    # ---------- REGISTROS DE PONTO (EVENTOS) ----------

    def registrar_entrada(self, matricula: str, instante: Optional[datetime] = None) -> None:
        """
        Registra um evento de ENTRADA.
        Não deixa ter duas entradas seguidas sem saída.
        """
        matricula = str(matricula)

        if matricula not in self._funcionarios:
            raise ValueError("Funcionário não encontrado.")

        ultimo = self._ultimo_evento(matricula)
        if ultimo and ultimo.tipo == "entrada":
            raise ValueError("Já existe uma entrada sem saída para este funcionário.")

        instante = instante or datetime.now()
        registro = RegistroPonto(matricula=matricula, timestamp=instante, tipo="entrada")
        self._adicionar_registro(registro)

    def registrar_saida(self, matricula: str, instante: Optional[datetime] = None) -> None:
        """
        Registra um evento de SAÍDA.
        Só permite se a última ação foi uma entrada.
        """
        matricula = str(matricula)

        if matricula not in self._funcionarios:
            raise ValueError("Funcionário não encontrado.")

        ultimo = self._ultimo_evento(matricula)
        if not ultimo or ultimo.tipo != "entrada":
            raise ValueError("Não há entrada em aberto para este funcionário.")

        instante = instante or datetime.now()
        registro = RegistroPonto(matricula=matricula, timestamp=instante, tipo="saida")
        self._adicionar_registro(registro)

    def _adicionar_registro(self, registro: RegistroPonto) -> None:
        self._registros.append(registro)
        self.attendance_repo.append(registro)  # persiste no CSV (append)

    def _ultimo_evento(self, matricula: str) -> Optional[RegistroPonto]:
        eventos = [r for r in self._registros if r.matricula == matricula]
        if not eventos:
            return None
        eventos.sort(key=lambda r: r.timestamp)
        return eventos[-1]

    # ---------- DATAFRAMES ----------

    def dataframe_funcionarios(self) -> pd.DataFrame:
        dados = [f.to_dict() for f in self._funcionarios.values()]
        return pd.DataFrame(dados, columns=["matricula", "nome", "idade", "turno"])

    def dataframe_registros(self) -> pd.DataFrame:
        dados = [r.to_dict() for r in self._registros]
        return pd.DataFrame(dados, columns=["matricula", "timestamp", "tipo"])

    # ---------- GRÁFICOS ----------

    def grafico_barras_por_idade(
        self,
        show: bool = True,
        save_path: Optional[Path | str] = None,
    ):
        """
        Gráfico de barras com funcionários ordenados por idade.

        - show=True: mostra o gráfico na tela (CLI)
        - save_path: caminho do arquivo PNG (se None, usa config.GRAFICO_IDADE)
        """
        df = self.dataframe_funcionarios()
        if df.empty:
            print("Nenhum funcionário cadastrado.")
            return None

        df_ordenado = df.sort_values("idade")

        fig, ax = plt.subplots()
        ax.bar(df_ordenado["nome"], df_ordenado["idade"])
        ax.set_xlabel("Funcionário")
        ax.set_ylabel("Idade")
        ax.set_title("Funcionários ordenados por idade")
        for label in ax.get_xticklabels():
            label.set_rotation(45)
            label.set_ha("right")
        fig.tight_layout()

        # salva na pasta graficos
        save_path = Path(save_path or GRAFICO_IDADE)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_path)

        if show:
            plt.show()

        return fig

    def grafico_pizza_por_turno(
        self,
        show: bool = True,
        save_path: Optional[Path | str] = None,
    ):
        """
        Gráfico de pizza com a distribuição de funcionários por turno.

        - show=True: mostra o gráfico na tela (CLI)
        - save_path: caminho do arquivo PNG (se None, usa config.GRAFICO_TURNO)
        """
        df = self.dataframe_funcionarios()
        if df.empty:
            print("Nenhum funcionário cadastrado.")
            return None

        contagem = df["turno"].value_counts()

        fig, ax = plt.subplots()
        ax.pie(contagem, labels=contagem.index, autopct="%1.1f%%")
        ax.set_title("Distribuição de funcionários por turno")
        fig.tight_layout()

        # salva na pasta graficos
        save_path = Path(save_path or GRAFICO_TURNO)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_path)

        if show:
            plt.show()

        return fig

    def __repr__(self) -> str:
        return (
            f"<SistemaPonto funcionarios={len(self._funcionarios)} "
            f"registros={len(self._registros)}>"
        )
