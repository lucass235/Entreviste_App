from dataclasses import dataclass
from enum import Enum
from typing import Optional


class PapelUsuario(Enum):
    ADMINISTRADOR = "Administrador"
    FUNCIONARIO = "Funcionário"


@dataclass
class Usuario:
    """
    Representa um usuário que interage com o sistema (ator do diagrama).

    - Administrador: não precisa de matrícula associada.
    - Funcionário: usa a matrícula do funcionário cadastrado.
    """
    papel: PapelUsuario
    matricula: Optional[str] = None

    @property
    def is_admin(self) -> bool:
        return self.papel == PapelUsuario.ADMINISTRADOR

    @property
    def is_funcionario(self) -> bool:
        return self.papel == PapelUsuario.FUNCIONARIO
