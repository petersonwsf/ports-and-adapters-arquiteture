# tests/domain/test_membro.py
from datetime import date
from decimal import Decimal

import pytest

from domain.erros import (
    LimiteDeEmprestimosExcedido,
    LivroIndisponivel,
    MembroComMultaPendente,
)
from domain.livro import Livro
from domain.membro import Membro
from domain.value_objects import Isbn

HOJE = date(2025, 1, 10)


def um_livro(n: int = 1) -> Livro:
    return Livro(Isbn(f"978000000000{n}"), f"Livro {n}")


def um_membro() -> Membro:
    return Membro("m1", "Ana")


def test_emprestar_marca_livro_como_indisponivel():
    livro, membro = um_livro(), um_membro()
    membro.emprestar(livro, HOJE)
    assert not livro.disponivel
    assert len(membro.emprestimos_ativos) == 1


def test_prazo_do_emprestimo_e_de_14_dias():
    emprestimo = um_membro().emprestar(um_livro(), HOJE)
    assert emprestimo.periodo.data_limite == date(2025, 1, 24)


def test_nao_permite_mais_de_3_emprestimos_ativos():
    membro = um_membro()
    for n in (1, 2, 3):
        membro.emprestar(um_livro(n), HOJE)
    with pytest.raises(LimiteDeEmprestimosExcedido):
        membro.emprestar(um_livro(4), HOJE)


def test_nao_empresta_livro_indisponivel():
    livro = um_livro()
    um_membro().emprestar(livro, HOJE)
    with pytest.raises(LivroIndisponivel):
        Membro("m2", "Bia").emprestar(livro, HOJE)


def test_devolucao_no_prazo_nao_gera_multa():
    livro, membro = um_livro(), um_membro()
    membro.emprestar(livro, HOJE)
    multa = membro.devolver(livro, date(2025, 1, 24))  # último dia
    assert not multa.existe()
    assert livro.disponivel
    assert membro.emprestimos_ativos == ()


def test_devolucao_atrasada_gera_multa_de_1_real_por_dia():
    livro, membro = um_livro(), um_membro()
    membro.emprestar(livro, HOJE)
    multa = membro.devolver(livro, date(2025, 1, 29))  # 5 dias de atraso
    assert multa.valor == Decimal("5.00")
    assert membro.multa_pendente == multa


def test_multa_pendente_bloqueia_novos_emprestimos():
    livro, membro = um_livro(), um_membro()
    membro.emprestar(livro, HOJE)
    membro.devolver(livro, date(2025, 1, 29))
    with pytest.raises(MembroComMultaPendente):
        membro.emprestar(um_livro(2), date(2025, 1, 29))


def test_quitar_multa_libera_novos_emprestimos():
    livro, membro = um_livro(), um_membro()
    membro.emprestar(livro, HOJE)
    membro.devolver(livro, date(2025, 1, 29))
    membro.quitar_multas()
    membro.emprestar(um_livro(2), date(2025, 1, 29))  # não lança erro