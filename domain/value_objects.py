from dataclasses import dataclass
from datetime import date, timedelta
from decimal import Decimal

PRAZO_EM_DIAS = 14


@dataclass(frozen=True)
class Isbn:
    valor: str

    def __post_init__(self):
        limpo = self.valor.replace("-", "")
        if not (limpo.isdigit() and len(limpo) == 13):
            raise ValueError(f"ISBN inválido: {self.valor}")
        object.__setattr__(self, "valor", limpo)  # normaliza (frozen exige isso)


@dataclass(frozen=True)
class Multa:
    valor: Decimal

    def __post_init__(self):
        if self.valor < 0:
            raise ValueError("Multa não pode ser negativa")

    @classmethod
    def zero(cls) -> "Multa":
        return cls(Decimal("0"))

    def existe(self) -> bool:
        return self.valor > 0

    def somar(self, outra: "Multa") -> "Multa":
        return Multa(self.valor + outra.valor)


@dataclass(frozen=True)
class PeriodoDeEmprestimo:
    retirada: date

    @property
    def data_limite(self) -> date:
        return self.retirada + timedelta(days=PRAZO_EM_DIAS)

    def dias_de_atraso(self, em: date) -> int:
        return max(0, (em - self.data_limite).days)