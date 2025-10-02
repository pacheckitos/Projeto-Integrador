class Biblioteca:

    def __init__(self):
        self.livros = dict()
        self.leitores = dict()
        self.emprestimos = []

### CRUD LIVROS ###

    def cadastrar_livro(self, cod, titulo):
        livro = Livro()
        livro.set_cod(cod)
        livro.set_titulo(titulo)
        self.livros[livro.cod] = livro

    def consultar_livro(self, cod):
        try:
            return self.livros[cod]
        except KeyError:
            return False

    def excluir_livro(self, cod):
        try:
            del self.livros[cod]
            return True
        except KeyError:
            return False

    def atualizar_livro(self, livro, cod, titulo):
        self.excluir_livro(livro.cod)
        self.cadastrar_livro(cod, titulo)

### CRUD LEITORES ###

    def cadastrar_leitor(self, cpf, nome):
        leitor = Leitor()
        leitor.set_cpf(cpf)
        leitor.set_nome(nome)
        self.leitores[leitor.cpf] = leitor

    def consultar_leitor(self, cpf):
        try:
            return self.leitores[cpf]
        except KeyError:
            return False

    def excluir_leitor(self, cpf):
        try:
            del self.leitores[cpf]
            return True
        except KeyError:
            return False

    def atualizar_leitor(self, leitor, nome, cpf):
        self.excluir_leitor(leitor.cpf)
        self.cadastrar_leitor(cpf, nome)
        

### "CRUD" EMPRESTIMOS ###

    def emprestar(self, livro, leitor):
        data_de_devolucao = self.calcular_data_devolucao()
        cod = self.codigo_emprestimo()
        livro.set_emprestado()
        novo_emprestimo = Emprestimo(livro, leitor, data_de_devolucao, cod)
        self.emprestimos.append(novo_emprestimo)
        return novo_emprestimo

    def consultar_emprestimo(self, cod):
        for e in self.emprestimos:
            if e.livro.cod == cod:
                return e

    def devolver(self, emprestimo):
        try:
            emprestimo.livro.set_devolvido()
            self.emprestimos.remove(emprestimo)
            return True
        except KeyError:
            return False
        
    def calcular_data_devolucao(self):
        import datetime
        hoje = datetime.date.today()
        tempo_de_emprestimo = datetime.timedelta(weeks=1)
        # somamos 1 semana à data de emprestimo
        return hoje + tempo_de_emprestimo

    def codigo_emprestimo(self):
        # implementar lógica que gera unicos de empréstimo
        # range: 0001 a 9999
        if not biblioteca.emprestimos:
            return "0001"
        else:
            ultimo_codigo = biblioteca.emprestimos[-1].cod
            novo_codigo = int(ultimo_codigo) + 1
            return str(novo_codigo).zfill(4)

class Emprestimo:

    def __init__(self, livro, leitor, data_devolucao, cod):
        self.livro = livro
        self.leitor = leitor
        self.data_devolucao = data_devolucao
        self.cod = biblioteca.codigo_emprestimo()

class Leitor:
    def __init__(self):
        self.emprestimos = list()

    def set_nome(self, nome):
        self.nome = nome

    def set_cpf(self, cpf):
        cpf = str(cpf)
        self.cpf = cpf

    def add_emprestimo(self, emprestimo):
        self.emprestimos.append(emprestimo)

class Livro:
    def __init__(self):
        self.emprestado = False

    def set_titulo(self, titulo):
        self.titulo = titulo

    def set_cod(self, cod):
        self.cod = cod

    def set_emprestado(self):
        self.emprestado = True

    def set_devolvido(self):
        self.emprestado = False

# instância única da "base de dados" para conexao com control e view

biblioteca = Biblioteca()

# "pacotes de dados usados em transações que envolvem várias telas (globais)"

LIVRO = None
LEITOR = None