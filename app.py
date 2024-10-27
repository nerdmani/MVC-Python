import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

class BibliotecaDB:
    def __init__(self, db_name="biblioteca.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.criar_tabelas()

    def criar_tabelas(self):
        # Tabela de livros
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS livros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            isbn TEXT UNIQUE NOT NULL,
            disponivel INTEGER DEFAULT 1
        )
        """)

        # Tabela de usuários
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
        """)

        # Tabela de empréstimos
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS emprestimos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            livro_id INTEGER,
            usuario_id INTEGER,
            data_emprestimo TEXT,
            FOREIGN KEY (livro_id) REFERENCES livros (id),
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
        )
        """)

        self.conn.commit()

    def adicionar_livro(self, titulo, autor, isbn):
        self.cursor.execute("INSERT INTO livros (titulo, autor, isbn) VALUES (?, ?, ?)", (titulo, autor, isbn))
        self.conn.commit()

    def adicionar_usuario(self, nome, email):
        self.cursor.execute("INSERT INTO usuarios (nome, email) VALUES (?, ?)", (nome, email))
        self.conn.commit()

    def emprestar_livro(self, livro_id, usuario_id):
        self.cursor.execute("INSERT INTO emprestimos (livro_id, usuario_id, data_emprestimo) VALUES (?, ?, datetime('now'))", (livro_id, usuario_id))
        self.conn.commit()

    def visualizar_emprestimos(self):
        self.cursor.execute("""
        SELECT l.titulo, u.nome, e.data_emprestimo 
        FROM emprestimos e 
        JOIN livros l ON e.livro_id = l.id 
        JOIN usuarios u ON e.usuario_id = u.id
        """)
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()


class BibliotecaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gerenciamento de Biblioteca")
        self.db = BibliotecaDB()

        # Criar Interface
        self.create_widgets()

    def create_widgets(self):
        # Cadastro de livro
        self.titulo_entry = tk.Entry(self.root, width=30)
        self.titulo_entry.pack()
        self.titulo_entry.insert(0, "Título do Livro")

        self.autor_entry = tk.Entry(self.root, width=30)
        self.autor_entry.pack()
        self.autor_entry.insert(0, "Autor do Livro")

        self.isbn_entry = tk.Entry(self.root, width=30)
        self.isbn_entry.pack()
        self.isbn_entry.insert(0, "ISBN do Livro")

        self.adicionar_livro_btn = tk.Button(self.root, text="Adicionar Livro", command=self.adicionar_livro)
        self.adicionar_livro_btn.pack()

        # Cadastro de usuário
        self.nome_entry = tk.Entry(self.root, width=30)
        self.nome_entry.pack()
        self.nome_entry.insert(0, "Nome do Usuário")

        self.email_entry = tk.Entry(self.root, width=30)
        self.email_entry.pack()
        self.email_entry.insert(0, "Email do Usuário")

        self.adicionar_usuario_btn = tk.Button(self.root, text="Adicionar Usuário", command=self.adicionar_usuario)
        self.adicionar_usuario_btn.pack()

        # Empréstimos
        self.emprestar_btn = tk.Button(self.root, text="Registrar Empréstimo", command=self.registrar_emprestimo)
        self.emprestar_btn.pack()

        # Visualizar Empréstimos
        self.visualizar_btn = tk.Button(self.root, text="Visualizar Empréstimos", command=self.visualizar_emprestimos)
        self.visualizar_btn.pack()

    def adicionar_livro(self):
        titulo = self.titulo_entry.get()
        autor = self.autor_entry.get()
        isbn = self.isbn_entry.get()
        self.db.adicionar_livro(titulo, autor, isbn)
        messagebox.showinfo("Sucesso", "Livro adicionado com sucesso!")

    def adicionar_usuario(self):
        nome = self.nome_entry.get()
        email = self.email_entry.get()
        self.db.adicionar_usuario(nome, email)
        messagebox.showinfo("Sucesso", "Usuário adicionado com sucesso!")

    def registrar_emprestimo(self):
        livro_id = simpledialog.askinteger("Empréstimo", "ID do Livro:")
        usuario_id = simpledialog.askinteger("Empréstimo", "ID do Usuário:")
        self.db.emprestar_livro(livro_id, usuario_id)
        messagebox.showinfo("Sucesso", "Empréstimo registrado com sucesso!")

    def visualizar_emprestimos(self):
        emprestimos = self.db.visualizar_emprestimos()
        if not emprestimos:
            messagebox.showinfo("Empréstimos", "Nenhum empréstimo registrado.")
            return
        
        info = "\n".join([f"{livro} - {usuario} - {data}" for livro, usuario, data in emprestimos])
        messagebox.showinfo("Empréstimos", info)

    def close(self):
        self.db.close()


if __name__ == "__main__":
    root = tk.Tk()
    app = BibliotecaApp(root)
    root.protocol("WM_DELETE_WINDOW", app.close)
    root.mainloop()
