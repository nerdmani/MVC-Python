from model.emprestimo import Emprestimo

class EmprestimoController:
    def __init__(self):
        self.emprestimos = []

    def realizar_emprestimo(self, livro, usuario):
        if livro.disponivel:
            emprestimo = Emprestimo(livro, usuario)
            livro.disponivel = False
            usuario.livros_emprestados.append(livro)
            self.emprestimos.append(emprestimo)
            return "Empréstimo realizado com sucesso!"
        return "Livro indisponível para empréstimo."

    def realizar_devolucao(self, livro, usuario):
        emprestimo = next((e for e in self.emprestimos if e.livro == livro and e.ativo), None)
        if emprestimo:
            emprestimo.ativo = False
            livro.disponivel = True
            usuario.livros_emprestados.remove(livro)
            return "Devolução realizada com sucesso!"
        return "Empréstimo não encontrado."
