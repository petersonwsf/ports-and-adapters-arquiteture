from application.erros import LivroNaoEncontrado, MembroNaoEncontrado
from application.ports.in_.emprestar_livro import (
    EmprestarLivro,
    EmprestarLivroComando,
    EmprestimoRealizado,
)
from application.ports.out.livro_repository import LivroRepository
from application.ports.out.membro_repository import MembroRepository
from application.ports.out.notificador import Notificador
from application.ports.out.relogio import Relogio
from domain.eventos import LivroEmprestado
from domain.value_objects import Isbn


class EmprestarLivroUseCase(EmprestarLivro):
    def __init__(
        self,
        membros: MembroRepository,
        livros: LivroRepository,
        relogio: Relogio,
        notificador: Notificador,
    ):
        self._membros = membros
        self._livros = livros
        self._relogio = relogio
        self._notificador = notificador

    def executar(self, comando: EmprestarLivroComando) -> EmprestimoRealizado:
        membro = self._membros.buscar_por_id(comando.membro_id)
        if membro is None:
            raise MembroNaoEncontrado(comando.membro_id)

        isbn = Isbn(comando.isbn)
        livro = self._livros.buscar_por_isbn(isbn)
        if livro is None:
            raise LivroNaoEncontrado(comando.isbn)

        hoje = self._relogio.hoje()
        emprestimo = membro.emprestar(livro, hoje)

        self._livros.salvar(livro)
        self._membros.salvar(membro)

        self._notificador.notificar_emprestimo(
            LivroEmprestado(
                membro_id=membro.id,
                isbn=livro.isbn,
                titulo=livro.titulo,
                data_limite=emprestimo.periodo.data_limite,
            )
        )

        return EmprestimoRealizado(
            emprestimo_id=emprestimo.id,
            isbn=livro.isbn.valor,
            titulo=livro.titulo,
            data_limite=emprestimo.periodo.data_limite,
        )