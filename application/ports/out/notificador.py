from typing import Protocol
from domain.eventos import LivroEmprestado


class Notificador(Protocol):
    def notificar_emprestimo(self, evento: LivroEmprestado) -> None: ...