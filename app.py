from textual.app import App, SystemCommand
from textual.binding import Binding
from view import TelaInicial, TelaMenuLivros, TelaMenuLeitores, TelaMenuEmprestimos, TelaMenuLeitores, TelaAtualizaLeitor, TelaAtualizaLivro

class AppBiblioteca(App):

    BINDINGS = [
        Binding("escape", "ir_para_inicial", "Início"),
        Binding("ctrl+n", "menu_livros", "Menu de livros"),
        Binding("ctrl+l", "menu_leitores", "Menu de Leitores"),
        Binding("ctrl+e", "menu_emprestimos", "Menu de empréstimos")
    ]

    SCREENS = {
        "inicial" : TelaInicial,
        "menu_livros" : TelaMenuLivros,
        "menu_leitores" : TelaMenuLeitores,
        "menu_emprestimos" : TelaMenuEmprestimos,
        "atualizacao_leitor" : TelaAtualizaLeitor,
        "atualizacao_livro" : TelaAtualizaLivro
    }

    def on_mount(self):
        self.push_screen("inicial")    

    def action_ir_para_inicial(self):
        self.switch_screen("inicial")

    def action_menu_livros(self):
        self.switch_screen("menu_livros")

    def action_menu_leitores(self):
        self.switch_screen("menu_leitores")

    def action_menu_emprestimos(self):
        self.switch_screen("menu_emprestimos")

    def get_system_commands(self, screen):
        yield from super().get_system_commands(screen)
        yield SystemCommand("Bell", "Ring the bell", self.action_cadastrar_livros)

if __name__ == "__main__":
    AppBiblioteca().run()