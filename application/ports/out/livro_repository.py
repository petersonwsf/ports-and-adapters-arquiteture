from typing import Protocol

from domain.livro import Livro
from domain.value_objects import Isbn


class LivroRepository(Protocol):
    def buscar_por_isbn(self, isbn: Isbn) -> Livro | None: ...
    def salvar(self, livro: Livro) -> None: ...