from datetime import date
from decimal import Decimal

from domain.value_objects import Multa, PeriodoDeEmprestimo

VALOR_POR_DIA = Decimal("1.00")


class CalculadoraDeMulta:
    def calcular(self, periodo: PeriodoDeEmprestimo, devolvido_em: date) -> Multa:
        dias = periodo.dias_de_atraso(devolvido_em)
        return Multa(VALOR_POR_DIA * dias)