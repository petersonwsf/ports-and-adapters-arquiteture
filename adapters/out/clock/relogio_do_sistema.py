from datetime import date

from application.ports.out.relogio import Relogio


class RelogioDoSistema(Relogio):
    def hoje(self) -> date:
        return date.today()