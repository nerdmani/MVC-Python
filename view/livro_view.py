from tabulate import tabulate

class LivroView:
    def mostrar_livros(self, livros):
        if not livros:
            print("Nenhum livro encontrado.")
            return

        tabela = [[livro.titulo, livro.autor, livro.isbn, "Disponível" if livro.disponivel else "Indisponível"] for livro in livros]
        cabecalho = ["Título", "Autor", "ISBN", "Status"]
        print(tabulate(tabela, headers=cabecalho, tablefmt="pretty"))
