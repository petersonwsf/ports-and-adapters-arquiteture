# application/use_cases/devolver_livro.py
from application.erros import LivroNaoEncontrado, MembroNaoEncontrado
from application.ports.in_.devolver_livro import (
    DevolucaoRealizada,
    DevolverLivro,
    DevolverLivroComando,
)
from application.ports.out.livro_repository import LivroRepository
from application.ports.out.membro_repository import MembroRepository
from application.ports.out.relogio import Relogio
from domain.calculadora_de_multa import CalculadoraDeMulta
from domain.value_objects import Isbn


class DevolverLivroUseCase(DevolverLivro):
    def __init__(
        self,
        membros: MembroRepository,
        livros: LivroRepository,
        relogio: Relogio,
        calculadora: CalculadoraDeMulta | None = None,
    ):
        self._membros = membros
        self._livros = livros
        self._relogio = relogio
        self._calculadora = calculadora or CalculadoraDeMulta()

    def executar(self, comando: DevolverLivroComando) -> DevolucaoRealizada:
        membro = self._membros.buscar_por_id(comando.membro_id)
        if membro is None:
            raise MembroNaoEncontrado(comando.membro_id)

        livro = self._livros.buscar_por_isbn(Isbn(comando.isbn))
        if livro is None:
            raise LivroNaoEncontrado(comando.isbn)

        multa = membro.devolver(livro, self._relogio.hoje(), self._calculadora)

        self._livros.salvar(livro)
        self._membros.salvar(membro)

        return DevolucaoRealizada(
            isbn=livro.isbn.valor,
            titulo=livro.titulo,
            multa_aplicada=multa.valor,
            multa_total_pendente=membro.multa_pendente.valor,
        )