import copy

from application.ports.out.livro_repository import LivroRepository
from application.ports.out.membro_repository import MembroRepository
from domain.livro import Livro
from domain.membro import Membro
from domain.value_objects import Isbn


class MembroRepositoryEmMemoria(MembroRepository):
    def __init__(self, *membros: Membro):
        self._dados: dict[str, Membro] = {m.id: copy.deepcopy(m) for m in membros}

    def buscar_por_id(self, membro_id: str) -> Membro | None:
        membro = self._dados.get(membro_id)
        return copy.deepcopy(membro) if membro else None

    def salvar(self, membro: Membro) -> None:
        self._dados[membro.id] = copy.deepcopy(membro)


class LivroRepositoryEmMemoria(LivroRepository):
    def __init__(self, *livros: Livro):
        self._dados: dict[Isbn, Livro] = {l.isbn: copy.deepcopy(l) for l in livros}

    def buscar_por_isbn(self, isbn: Isbn) -> Livro | None:
        livro = self._dados.get(isbn)
        return copy.deepcopy(livro) if livro else None

    def salvar(self, livro: Livro) -> None:
        self._dados[livro.isbn] = copy.deepcopy(livro)