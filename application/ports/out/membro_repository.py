from typing import Protocol

from domain.membro import Membro


class MembroRepository(Protocol):
    def buscar_por_id(self, membro_id: str) -> Membro | None: ...
    def salvar(self, membro: Membro) -> None: ...