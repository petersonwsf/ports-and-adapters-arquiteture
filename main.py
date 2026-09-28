# main.py
from adapters.in_.cli.app import CliApp
from adapters.out.clock.relogio_do_sistema import RelogioDoSistema
from adapters.out.notification.console import NotificadorDeConsole
from adapters.out.persistence.memoria import (
    LivroRepositoryEmMemoria,
    MembroRepositoryEmMemoria,
)
from application.uses_cases.devolver_livro import DevolverLivroUseCase
from application.uses_cases.emprestar_livro import EmprestarLivroUseCase
from domain.emprestimo import Emprestimo
from domain.livro import Livro
from domain.membro import Membro
from domain.value_objects import Isbn
from datetime import date


def dados_de_demonstracao() -> tuple[list[Membro], list[Livro]]:
    livros = [
        Livro(Isbn("9780000000001"), "Domain-Driven Design"),
        Livro(Isbn("9780000000002"), "Clean Architecture"),
        Livro(Isbn("9780000000003"), "Refactoring", disponivel=False),
        Livro(Isbn("9780000000004"), "Test-Driven Development"),
    ]
    atrasado = Emprestimo.iniciar(livros[2].isbn, "m3", date(2025, 1, 10))
    membros = [
        Membro("m1", "Ana"),
        Membro("m2", "Bruno"),
        Membro("m3", "Carla", emprestimos_ativos=[atrasado]),
    ]
    return membros, livros


def montar_cli() -> CliApp:
    membros_iniciais, livros_iniciais = dados_de_demonstracao()

    membros = MembroRepositoryEmMemoria(*membros_iniciais)
    livros = LivroRepositoryEmMemoria(*livros_iniciais)
    relogio = RelogioDoSistema()
    notificador = NotificadorDeConsole()

    emprestar = EmprestarLivroUseCase(membros, livros, relogio, notificador)
    devolver = DevolverLivroUseCase(membros, livros, relogio)

    return CliApp(emprestar, devolver)


if __name__ == "__main__":
    montar_cli().executar_loop()