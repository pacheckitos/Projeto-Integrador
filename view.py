from textual import on
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Input, Button, TabbedContent, TabPane, Markdown
from model import biblioteca

class TelaInicial(Screen):
    def compose(self):
        yield Header(show_clock = True)
        yield Static("Bem-vindo à biblioteca. Selecione um menu para realizar operações.")
        yield Button("Menu de leitores", id = "button_menu_leitores")
        yield Button("Menu de livros", id = "button_menu_livros")
        yield Button("Empréstimos", id = "button_menu_emprestimos") 
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed):
        match event.button.id:
            case "button_menu_leitores":
                self.app.switch_screen("menu_leitores")
            case "button_menu_livros":
                self.app.switch_screen("menu_livros")
            case "button_menu_emprestimos":
                self.app.switch_screen("menu_emprestimos")

class TelaMenuLivros(Screen):
    def compose(self):
        yield Header(show_clock = True)
        with TabbedContent():
            
            with TabPane("Cadastrar livro", id="tab_cadastrar_livro"):
                yield Static("Informe o título do livro:")
                yield Input(placeholder = "Título", id = "cadastro_titulo_livro")
                yield Static("Informe o códido de cadastro do livro:")
                yield Input(placeholder = "Código de cadastro", id = "cadastro_codigo_livro")
                yield Button("Cadastrar livro", id = "button_cadastrar_livro")
            
            with TabPane("Excluir livro", id="tab_excluir_livro"):
                yield Static("Informe o código de cadastro do livro:")
                yield Input(placeholder = "Código de cadastro", id = "excluir_codigo_livro")
                yield Button("Excluir livro", id = "button_excluir_livro")
            
            with TabPane("Atualizar livro", id="tab_atualizar_livro"):
                yield Static("Informe o código de cadastro do livro:")
                yield Input(placeholder = "Código de cadastro", id = "buscar_codigo_livro")
                yield Button("Buscar", id = "button_busca_livro")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed):
        match event.button.id:
            case "button_cadastrar_livro":
                titulo = self.query_one("#cadastro_titulo_livro").value
                codigo = self.query_one("#cadastro_codigo_livro").value
                biblioteca.cadastrar_livro(codigo, titulo)
                self.notify(f"Cadastro realizado!\nLivro: {titulo}\nCódigo: {codigo}")
                cadastro_titulo_livro = self.query_one("#cadastro_titulo_livro")
                cadastro_codigo_livro = self.query_one("#cadastro_codigo_livro")
                cadastro_titulo_livro.value = ""
                cadastro_codigo_livro.value = ""
                cadastro_titulo_livro.focus()

            case "button_excluir_livro":
                cod = self.query_one("#excluir_codigo_livro").value
                if biblioteca.excluir_livro(cod):
                    self.notify(f"Cadastro excluído!\nCódigo: {cod}")
                else:
                    self.notify(f"Erro!\nLivro não encontrado para o código {cod}")
                excluir_codigo_livro = self.query_one("#excluir_codigo_livro")
                excluir_codigo_livro.value = ""
                excluir_codigo_livro.focus()

            case "button_busca_livro":
                codigo = self.query_one("#buscar_codigo_livro").value
                if biblioteca.consultar_livro(codigo) == False:
                    self.notify(f"Erro!\nLivro não encontrado para o código {codigo}")
                else:
                    biblioteca.LIVRO = biblioteca.consultar_livro(codigo)
                    self.app.switch_screen("atualizacao_livro")
                buscar_codigo_livro = self.query_one("#buscar_codigo_livro")
                buscar_codigo_livro.value = ""                

class TelaAtualizaLivro(Screen):
    def compose(self):
        yield Header(show_clock = True)
        yield Static("Informe o novo título do livro:")
        yield Input(placeholder = "Título", id = "atualizacao_titulo_livro")
        yield Static("Informe o novo código do livro:")
        yield Input(placeholder = "Código", id = "atualizacao_codigo_livro")
        yield Button("Atualizar livro", id = "atualizacao_cadastro_livro")
        yield Footer()

    @on(Button.Pressed, "#atualizacao_cadastro_livro")
    def atualiza_livro(self):
        novo_codigo = self.query_one("#atualizacao_codigo_livro").value
        novo_titulo = self.query_one("#atualizacao_titulo_livro").value
        biblioteca.atualizar_livro(biblioteca.LIVRO, novo_codigo, novo_titulo)
        self.limpar()
        biblioteca.LIVRO = None # Mesmas alterações do excluir + cadastrar
        self.notify(f"Cadastro alterado!\nTítulo: {novo_titulo}\nCódigo: {novo_codigo}")
        self.app.switch_screen("menu_livros")

    def limpar(self):
        atualizacao_codigo_livro = self.query_one("#atualizacao_codigo_livro")
        atualizacao_titulo_livro = self.query_one("#atualizacao_titulo_livro")
        atualizacao_codigo_livro.value = ""
        atualizacao_titulo_livro.value = ""
        atualizacao_titulo_livro.focus()

class TelaMenuLeitores(Screen):
    def compose(self):
        yield Header(show_clock = True)
        with TabbedContent():

            with TabPane("Cadastrar leitor", id = "tab_cadastrar_leitor"):
                yield Static("Informe o nome do leitor:")
                yield Input(placeholder = "Nome completo", id ="cadastro_nome_leitor")
                yield Static("Informe o CPF do leitor:")
                yield Input(placeholder = "CPF", id = "cadastro_cpf_leitor")
                yield Button("Cadastrar leitor", id = "button_cadastrar_leitor")

            
            with TabPane("Excluir leitor", id = "tab_excluir_leitor"):
                yield Static("Informe o CPF do leitor:")
                yield Input(placeholder = "CPF", id = "txt_excluir_leitor")
                yield Button("Excluir leitor", id = "button_excluir_leitor")
            
            with TabPane("Atualizar leitor", id = "tab_atualizar_leitor"):
                yield Static("Informe o CPF do leitor:")
                yield Input(placeholder = "CPF", id = "txt_busca_leitor")
                yield Button("Buscar", id = "button_busca_atualiza_leitor")             
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed):
        match event.button.id:
            case "button_cadastrar_leitor":
                cadastro_nome_leitor = self.query_one("#cadastro_nome_leitor")
                cadastro_cpf_leitor = self.query_one("#cadastro_cpf_leitor")
                cpf = self.query_one("#cadastro_cpf_leitor").value                
                nome = self.query_one("#cadastro_nome_leitor").value
                biblioteca.cadastrar_leitor(cpf, nome)
                cadastro_nome_leitor.value = ""
                cadastro_cpf_leitor.value = ""
                cadastro_nome_leitor.focus()
                self.notify(f"Cadastro realizado! \nNome: {nome} \nCPF: {cpf}")
        
            case "button_excluir_leitor":
                cpf = self.query_one("#txt_excluir_leitor").value
                if biblioteca.excluir_leitor(cpf):
                    self.notify(f"Cadastro excluído!\nCPF: {cpf}")
                else:
                    self.notify(f"Erro!\nLeitor não encontrado para o CPF {cpf}")
                txt_excluir_leitor = self.query_one("#txt_excluir_leitor")
                txt_excluir_leitor.value = ""
                txt_excluir_leitor.focus()

            case "button_busca_atualiza_leitor":
                txt_busca_leitor = self.query_one("#txt_busca_leitor")
                cpf = self.query_one("#txt_busca_leitor").value
                if biblioteca.consultar_leitor(cpf) == False:
                    txt_busca_leitor.value = ""
                    txt_busca_leitor.focus()
                    self.notify(f"Erro!\nLeitor não encontrado para o CPF {cpf}")

                else:
                    txt_busca_leitor.value = ""
                    txt_busca_leitor.focus()
                    biblioteca.LEITOR = biblioteca.consultar_leitor(cpf)
                    self.app.switch_screen("atualizacao_leitor")
                    # Chama outra tela para realizar a atualização

class TelaAtualizaLeitor(Screen):
    def compose(self):
        yield Header(show_clock = True)
        yield Static("Informe o novo nome do leitor:")
        yield Input(placeholder = "Nome completo", id = "atualizacao_nome_leitor")
        yield Static("Informe o novo CPF do leitor:")
        yield Input(placeholder = "CPF", id = "atualizacao_cpf_leitor")
        yield Button("Atualizar leitor", id = "atualizacao_cadastrar_leitor")
        yield Footer()

    @ on(Button.Pressed, "#atualizacao_cadastrar_leitor")
    def atualiza_leitor(self):
        novo_cpf = self.query_one("#atualizacao_cpf_leitor").value
        novo_nome = self.query_one("#atualizacao_nome_leitor").value
        biblioteca.atualizar_leitor(biblioteca.LEITOR, novo_nome, novo_cpf)
        self.limpar()
        biblioteca.LEITOR = None
        self.notify(f"Cadastro alterado! \nNome: {novo_nome} \nCPF: {novo_cpf}")
        self.app.switch_screen("menu_leitores")

    def limpar(self):
        atualizacao_cpf_leitor = self.query_one("#atualizacao_cpf_leitor")
        atualizacao_nome_leitor = self.query_one("#atualizacao_nome_leitor")
        atualizacao_cpf_leitor.value = ""
        atualizacao_nome_leitor.value = ""
        atualizacao_nome_leitor.focus()

class TelaMenuEmprestimos(Screen):
    def compose(self):
        yield Header(show_clock = True)
        with TabbedContent():
            
            with TabPane("Criar empréstimo", id = "tab_criar_emprestimo"):
                yield Static("Informe o CPF do leitor:")
                yield Input(placeholder = "CPF", id="busca_cpf_leitor")
                yield Static("Informe o código de cadastro do livro:")
                yield Input(placeholder = "Código de cadastro", id="busca_codigo_livro")
                yield Button("Criar empréstimo", id = "button_criar_emprestimo")
                '''yield Markdown(f"### Empréstimos realizados:\n{"aaa"}")''' #ferramenta pra criar markdowns no sistema

            with TabPane("Registrar devolução", id = "tab_registrar_devolucao"):
                yield Static("Informe o CPF do leitor:")
                yield Input(placeholder = "CPF")
                yield Button("Buscar empréstimos do leitor", id = "button_buscar_emprestimos_1")

            with TabPane("Listar empréstimos", id = "tab_buscar_emprestimos"):
                yield Static("Informe o CPF do leitor:")
                yield Input(placeholder = "CPF")
                yield Button("Buscar empréstimos do leitor", id = "button_buscar_emprestimos_2")
        yield Footer()

    def limpar_criacao(self):
        busca_cpf_leitor = self.query_one("#busca_cpf_leitor")
        busca_codigo_livro = self.query_one("#busca_codigo_livro")
        busca_cpf_leitor.value = ""
        busca_codigo_livro.value = ""
        busca_cpf_leitor.focus()

    def on_button_pressed(self, event: Button.Pressed):
        match event.button.id:
            case "button_criar_emprestimo":
                biblioteca.LEITOR = biblioteca.consultar_leitor(self.query_one("#busca_cpf_leitor").value)
                biblioteca.LIVRO = biblioteca.consultar_livro(self.query_one("#busca_codigo_livro").value)
                if biblioteca.LEITOR == None:
                    self.notify(f"Erro!\nLeitor não encontrado para o CPF {self.query_one('#busca_cpf_leitor').value}")
                    busca_cpf_leitor = self.query_one("#busca_cpf_leitor")
                    busca_cpf_leitor.value = ""
                    busca_cpf_leitor.focus()

                elif biblioteca.LIVRO == None:
                    self.notify(f"Erro!\nLivro não encontrado para o código {self.query_one('#busca_codigo_livro').value}")
                    busca_codigo_livro = self.query_one("#busca_codigo_livro")
                    busca_codigo_livro.value = ""
                    busca_codigo_livro.focus()

                else:
                    biblioteca.emprestar(biblioteca.LIVRO, biblioteca.LEITOR)
                    self.notify(f"Empréstimo realizado!\nLeitor: {biblioteca.LEITOR.nome}\nLivro: {biblioteca.LIVRO.titulo}\nData de devolução: {biblioteca.emprestimos[-1].data_devolucao}\n Código do empréstimo: {biblioteca.emprestimos[-1].cod}")
                    self.limpar_criacao()

                    