from typing import Callable

from application.ports.out.notificador import Notificador
from domain.eventos import LivroEmprestado


class NotificadorDeConsole(Notificador):
    def __init__(self, saida: Callable[[str], None] = print):
        self._saida = saida

    def notificar_emprestimo(self, evento: LivroEmprestado) -> None:
        self._saida(
            f"[NOTIFICAÇÃO] Membro {evento.membro_id}: você pegou "
            f"'{evento.titulo}'. Devolva até {evento.data_limite:%d/%m/%Y}."
        )