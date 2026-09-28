from datetime import date

from domain.calculadora_de_multa import CalculadoraDeMulta
from domain.emprestimo import Emprestimo
from domain.erros import (
    EmprestimoNaoEncontrado,
    LimiteDeEmprestimosExcedido,
    MembroComMultaPendente,
)
from domain.livro import Livro
from domain.value_objects import Multa

LIMITE_DE_EMPRESTIMOS = 3


class Membro:
    def __init__(
        self,
        id: str,
        nome: str,
        emprestimos_ativos: list[Emprestimo] | None = None,
        multa_pendente: Multa | None = None,
    ):
        self.id = id
        self.nome = nome
        self._emprestimos_ativos = list(emprestimos_ativos or [])
        self._multa_pendente = multa_pendente or Multa.zero()

    @property
    def emprestimos_ativos(self) -> tuple[Emprestimo, ...]:
        return tuple(self._emprestimos_ativos)

    @property
    def multa_pendente(self) -> Multa:
        return self._multa_pendente

    def emprestar(self, livro: Livro, hoje: date) -> Emprestimo:
        # Regras do membro primeiro; só depois mexemos no livro,
        # para não deixar estado pela metade se algo falhar.
        if self._multa_pendente.existe():
            raise MembroComMultaPendente(self.id)
        if len(self._emprestimos_ativos) >= LIMITE_DE_EMPRESTIMOS:
            raise LimiteDeEmprestimosExcedido(self.id)

        livro.emprestar()  # lança LivroIndisponivel se for o caso

        emprestimo = Emprestimo.iniciar(livro.isbn, self.id, hoje)
        self._emprestimos_ativos.append(emprestimo)
        return emprestimo

    def devolver(
        self,
        livro: Livro,
        hoje: date,
        calculadora: CalculadoraDeMulta | None = None,
    ) -> Multa:
        calculadora = calculadora or CalculadoraDeMulta()
        emprestimo = next(
            (e for e in self._emprestimos_ativos if e.isbn == livro.isbn), None
        )
        if emprestimo is None:
            raise EmprestimoNaoEncontrado(str(livro.isbn.valor))

        emprestimo.devolver(hoje)
        multa = calculadora.calcular(emprestimo.periodo, hoje)
        livro.devolver()

        self._emprestimos_ativos.remove(emprestimo)
        self._multa_pendente = self._multa_pendente.somar(multa)
        return multa

    def quitar_multas(self) -> None:
        self._multa_pendente = Multa.zero()