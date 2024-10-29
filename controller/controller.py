from model.models import BibliotecaDB
from view.views import BibliotecaView
import tkinter as tk
from tkinter import messagebox, simpledialog

class BibliotecaController:
    def __init__(self, root):
        self.db = BibliotecaDB()
        self.view = BibliotecaView(root, self)

    def adicionar_livro(self):
        titulo = self.view.titulo_entry.get()
        autor = self.view.autor_entry.get()
        isbn = self.view.isbn_entry.get()
        sucesso = self.db.adicionar_livro(titulo, autor, isbn)
        if sucesso:
            messagebox.showinfo("Sucesso", "Livro adicionado com sucesso!")
        else:
            messagebox.showerror("Erro", "ISBN já cadastrado.")

    def adicionar_usuario(self):
        nome = self.view.nome_entry.get()
        email = self.view.email_entry.get()
        sucesso = self.db.adicionar_usuario(nome, email)
        if sucesso:
            messagebox.showinfo("Sucesso", "Usuário adicionado com sucesso!")
        else:
            messagebox.showerror("Erro", "Email já cadastrado.")

    def registrar_emprestimo(self):
        livro_isbn = simpledialog.askstring("Empréstimo", "ISBN do Livro:")
        usuario_id = simpledialog.askinteger("Empréstimo", "ID do Usuário:")
        sucesso = self.db.emprestar_livro(livro_isbn, usuario_id)
        if sucesso:
            messagebox.showinfo("Sucesso", "Empréstimo registrado!")
        else:
            messagebox.showerror("Erro", "Livro não disponível.")

    def devolver_livro(self):
        livro_isbn = simpledialog.askstring("Devolução", "ISBN do Livro:")
        sucesso = self.db.devolver_livro(livro_isbn)
        if sucesso:
            messagebox.showinfo("Sucesso", "Livro devolvido!")
        else:
            messagebox.showerror("Erro", "Erro ao devolver o livro.")

    def mostrar_emprestimos(self):
        emprestimos = self.db.visualizar_emprestimos()
        self.view.emprestimos_text.delete(1.0, tk.END)
        for emp in emprestimos:
            self.view.emprestimos_text.insert(tk.END, f"Livro: {emp[0]}, Usuário: {emp[1]}, Data: {emp[2]}\n")

    def mostrar_livros(self):
        livros = self.db.visualizar_livros()
        self.view.livros_text.delete(1.0, tk.END)
        for livro in livros:
            status = "Disponível" if livro[3] else "Indisponível"
            self.view.livros_text.insert(tk.END, f"{livro[0]}, {livro[1]}, {livro[2]}, {status}\n")

    def buscar_livro(self, isbn):
        livro = self.db.buscar_livro_por_isbn(isbn)
        if livro is None:
            messagebox.showinfo("Erro", "Livro não encontrado.")
        else:
            messagebox.showinfo("Livro encontrado", f"Título: {livro['titulo']}, Autor: {livro['autor']}, Disponível: {'Sim' if livro['disponivel'] else 'Não'}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BibliotecaController(root)
    root.mainloop()
