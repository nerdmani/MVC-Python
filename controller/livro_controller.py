from model.livro import Livro

class LivroController:
    def __init__(self):
        self.livros = []

    def cadastrar_livro(self, titulo, autor, isbn):
        livro = Livro(titulo, autor, isbn)
        self.livros.append(livro)
        return "Livro cadastrado com sucesso!"

    def consultar_livro(self, termo):
        return [livro for livro in self.livros if termo.lower() in livro.titulo.lower() or termo.lower() in livro.autor.lower()]
