from domain.erros import LivroIndisponivel
from domain.value_objects import Isbn


class Livro:
    def __init__(self, isbn: Isbn, titulo: str, disponivel: bool = True):
        self.isbn = isbn
        self.titulo = titulo
        self._disponivel = disponivel

    @property
    def disponivel(self) -> bool:
        return self._disponivel

    def emprestar(self) -> None:
        if not self._disponivel:
            raise LivroIndisponivel(f"'{self.titulo}' já está emprestado")
        self._disponivel = False

    def devolver(self) -> None:
        self._disponivel = True