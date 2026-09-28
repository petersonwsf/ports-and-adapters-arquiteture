from decimal import Decimal
from typing import Callable

from application.erros import (
    LivroNaoEncontrado,
    MembroNaoEncontrado,
    RecursoNaoEncontrado,
)
from application.ports.in_.devolver_livro import DevolverLivro, DevolverLivroComando
from application.ports.in_.emprestar_livro import EmprestarLivro, EmprestarLivroComando
from domain.erros import (
    EmprestimoJaDevolvido,
    EmprestimoNaoEncontrado,
    ErroDeDominio,
    LimiteDeEmprestimosExcedido,
    LivroIndisponivel,
    MembroComMultaPendente,
)

MENSAGENS_DE_DOMINIO: dict[type[ErroDeDominio], str] = {
    LimiteDeEmprestimosExcedido: "Limite de 3 empréstimos ativos atingido.",
    LivroIndisponivel: "Este livro já está emprestado.",
    MembroComMultaPendente: "Existe multa pendente. Quite antes de pegar novos livros.",
    EmprestimoNaoEncontrado: "Este membro não tem empréstimo ativo desse livro.",
    EmprestimoJaDevolvido: "Este empréstimo já foi devolvido.",
}

AJUDA = """Comandos:
  emprestar <membro_id> <isbn>
  devolver  <membro_id> <isbn>
  ajuda
  sair"""


def _reais(valor: Decimal) -> str:
    return f"R$ {valor:.2f}".replace(".", ",")


class CliApp:
    def __init__(
        self,
        emprestar: EmprestarLivro,
        devolver: DevolverLivro,
        entrada: Callable[[str], str] = input,
        saida: Callable[[str], None] = print,
    ):
        self._emprestar = emprestar
        self._devolver = devolver
        self._entrada = entrada
        self._saida = saida

    def executar_loop(self) -> None:
        self._saida("Biblioteca. Digite 'ajuda' para ver os comandos.")
        while True:
            try:
                linha = self._entrada("> ")
            except EOFError:
                break
            if not self.processar(linha):
                break

    def processar(self, linha: str) -> bool:
        """Processa uma linha. Devolve False quando o usuário pede para sair."""
        partes = linha.split()
        if not partes:
            return True
        comando, *args = partes
        if comando == "sair":
            return False

        try:
            if comando == "emprestar" and len(args) == 2:
                self._fazer_emprestimo(*args)
            elif comando == "devolver" and len(args) == 2:
                self._fazer_devolucao(*args)
            elif comando == "ajuda":
                self._saida(AJUDA)
            else:
                self._saida("Comando inválido. Digite 'ajuda'.")
        except MembroNaoEncontrado as e:
            self._saida(f"Membro '{e.args[0]}' não encontrado.")
        except LivroNaoEncontrado as e:
            self._saida(f"Livro '{e.args[0]}' não encontrado.")
        except RecursoNaoEncontrado as e:
            self._saida(f"Não encontrado: {e}")
        except ErroDeDominio as e:
            self._saida(MENSAGENS_DE_DOMINIO.get(type(e), "Operação não permitida."))
        except ValueError as e:
            self._saida(f"Dado inválido: {e}")
        return True

    def _fazer_emprestimo(self, membro_id: str, isbn: str) -> None:
        r = self._emprestar.executar(EmprestarLivroComando(membro_id, isbn))
        self._saida(
            f"Empréstimo realizado: '{r.titulo}'. "
            f"Devolver até {r.data_limite:%d/%m/%Y}."
        )

    def _fazer_devolucao(self, membro_id: str, isbn: str) -> None:
        r = self._devolver.executar(DevolverLivroComando(membro_id, isbn))
        self._saida(f"Devolução registrada: '{r.titulo}'.")
        if r.multa_aplicada > 0:
            self._saida(
                f"Multa desta devolução: {_reais(r.multa_aplicada)}. "
                f"Total pendente: {_reais(r.multa_total_pendente)}."
            )
        else:
            self._saida("Sem multa.")