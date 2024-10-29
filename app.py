import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

class BibliotecaDB:
    def __init__(self, db_name="biblioteca.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS livros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT,
                autor TEXT,
                isbn TEXT UNIQUE,
                disponivel BOOLEAN DEFAULT TRUE
            );
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT,
                email TEXT UNIQUE
            );
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS emprestimos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                livro_isbn TEXT,
                usuario_id INTEGER,
                data_emprestimo TEXT,
                FOREIGN KEY (livro_isbn) REFERENCES livros(isbn),
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
            );
        """)
        self.conn.commit()

    def adicionar_livro(self, titulo, autor, isbn):
        try:
            self.cursor.execute("INSERT INTO livros (titulo, autor, isbn, disponivel) VALUES (?, ?, ?, ?)", 
                                (titulo, autor, isbn, True))
            self.conn.commit()
            messagebox.showinfo("Sucesso", "Livro adicionado com sucesso!")
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "ISBN já cadastrado.")

    def adicionar_usuario(self, nome, email):
        try:
            self.cursor.execute("INSERT INTO usuarios (nome, email) VALUES (?, ?)", (nome, email))
            self.conn.commit()
            messagebox.showinfo("Sucesso", "Usuário adicionado com sucesso!")
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "Email já cadastrado.")

    def emprestar_livro(self, livro_isbn, usuario_id):
        self.cursor.execute("SELECT disponivel FROM livros WHERE isbn = ?", (livro_isbn,))
        resultado = self.cursor.fetchone()
        if resultado and resultado[0] == 1:
            self.cursor.execute("INSERT INTO emprestimos (livro_isbn, usuario_id, data_emprestimo) VALUES (?, ?, datetime('now'))", (livro_isbn, usuario_id))
            self.cursor.execute("UPDATE livros SET disponivel = 0 WHERE isbn = ?", (livro_isbn,))
            self.conn.commit()
            messagebox.showinfo("Sucesso", "Empréstimo registrado com sucesso!")
        else:
            messagebox.showerror("Erro", "Livro não está disponível para empréstimo.")

    def devolver_livro(self, livro_isbn):
        # Verifica se o livro está emprestado antes de devolvê-lo
        self.cursor.execute("SELECT disponivel FROM livros WHERE isbn = ?", (livro_isbn,))
        resultado = self.cursor.fetchone()
        
        if resultado and resultado[0] == 0:  
            self.cursor.execute("UPDATE livros SET disponivel = 1 WHERE isbn = ?", (livro_isbn,))
            self.cursor.execute("DELETE FROM emprestimos WHERE livro_isbn = ?", (livro_isbn,))
            self.conn.commit()
            messagebox.showinfo("Sucesso", "Livro devolvido com sucesso!")
        else:
            messagebox.showerror("Erro", "Este livro já está disponível ou ISBN inválido.")

    def visualizar_emprestimos(self):
        self.cursor.execute("""
            SELECT l.titulo, u.nome, e.data_emprestimo, l.disponivel 
            FROM emprestimos e 
            JOIN livros l ON e.livro_isbn = l.isbn 
            JOIN usuarios u ON e.usuario_id = u.id
        """)
        return self.cursor.fetchall()

    def visualizar_livros(self):
        self.cursor.execute("SELECT titulo, autor, isbn, disponivel FROM livros")
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()

class BibliotecaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gerenciamento de Biblioteca")
        self.db = BibliotecaDB()

        self.tabControl = ttk.Notebook(root)
        
        self.cadastro_livro_frame = ttk.Frame(self.tabControl)
        self.cadastro_usuario_frame = ttk.Frame(self.tabControl)
        self.emprestimo_frame = ttk.Frame(self.tabControl)
        self.visualizacao_emprestimos_frame = ttk.Frame(self.tabControl)
        self.visualizacao_livros_frame = ttk.Frame(self.tabControl)
        
        self.tabControl.add(self.cadastro_livro_frame, text='Cadastro de Livro')
        self.tabControl.add(self.cadastro_usuario_frame, text='Cadastro de Usuário')
        self.tabControl.add(self.emprestimo_frame, text='Empréstimos')
        self.tabControl.add(self.visualizacao_emprestimos_frame, text='Visualizar Empréstimos')
        self.tabControl.add(self.visualizacao_livros_frame, text='Visualizar Livros')
        
        self.tabControl.pack(expand=1, fill="both")

        self.create_widgets()

    def create_widgets(self):

        self.titulo_entry = tk.Entry(self.cadastro_livro_frame, width=30)
        self.titulo_entry.insert(0, "Título do Livro")
        self.titulo_entry.pack(pady=5)

        self.autor_entry = tk.Entry(self.cadastro_livro_frame, width=30)
        self.autor_entry.insert(0, "Autor do Livro")
        self.autor_entry.pack(pady=5)

        self.isbn_entry = tk.Entry(self.cadastro_livro_frame, width=30)
        self.isbn_entry.insert(0, "ISBN do Livro")
        self.isbn_entry.pack(pady=5)

        self.adicionar_livro_btn = tk.Button(self.cadastro_livro_frame, text="Adicionar Livro", command=self.adicionar_livro)
        self.adicionar_livro_btn.pack(pady=5)

        self.nome_entry = tk.Entry(self.cadastro_usuario_frame, width=30)
        self.nome_entry.insert(0, "Nome do Usuário")
        self.nome_entry.pack(pady=5)

        self.email_entry = tk.Entry(self.cadastro_usuario_frame, width=30)
        self.email_entry.insert(0, "Email do Usuário")
        self.email_entry.pack(pady=5)

        self.adicionar_usuario_btn = tk.Button(self.cadastro_usuario_frame, text="Adicionar Usuário", command=self.adicionar_usuario)
        self.adicionar_usuario_btn.pack(pady=5)

        self.emprestar_btn = tk.Button(self.emprestimo_frame, text="Registrar Empréstimo", command=self.registrar_emprestimo)
        self.emprestar_btn.pack(pady=10)

        self.devolver_btn = tk.Button(self.emprestimo_frame, text="Devolver Livro", command=self.devolver_livro)
        self.devolver_btn.pack(pady=10)

        self.visualizar_emprestimos_btn = tk.Button(self.visualizacao_emprestimos_frame, text="Atualizar Lista de Empréstimos", command=self.mostrar_emprestimos)
        self.visualizar_emprestimos_btn.pack(pady=10)
        self.emprestimos_text = tk.Text(self.visualizacao_emprestimos_frame, width=50, height=10)
        self.emprestimos_text.pack(pady=5)

        self.visualizar_livros_btn = tk.Button(self.visualizacao_livros_frame, text="Atualizar Lista de Livros", command=self.mostrar_livros)
        self.visualizar_livros_btn.pack(pady=10)
        self.livros_text = tk.Text(self.visualizacao_livros_frame, width=50, height=10)
        self.livros_text.pack(pady=5)

    def adicionar_livro(self):
        titulo = self.titulo_entry.get()
        autor = self.autor_entry.get()
        isbn = self.isbn_entry.get()
        self.db.adicionar_livro(titulo, autor, isbn)

    def adicionar_usuario(self):
        nome = self.nome_entry.get()
        email = self.email_entry.get()
        self.db.adicionar_usuario(nome, email)

    def registrar_emprestimo(self):
        livro_isbn = simpledialog.askstring("Empréstimo", "ISBN do Livro:")
        usuario_id = simpledialog.askinteger("Empréstimo", "ID do Usuário:")
        self.db.emprestar_livro(livro_isbn, usuario_id)

    def devolver_livro(self):
        livro_isbn = simpledialog.askstring("Devolução", "Digite o ISBN do Livro a ser devolvido:")
        if livro_isbn:
            self.db.devolver_livro(livro_isbn)
        else:
            messagebox.showerror("Erro", "ISBN não fornecido para devolução.")

    def mostrar_emprestimos(self):
        emprestimos = self.db.visualizar_emprestimos()
        self.emprestimos_text.delete(1.0, tk.END)
        for titulo, nome, data, disponivel in emprestimos:
            status = "Disponível" if disponivel else "Emprestado"
            self.emprestimos_text.insert(tk.END, f"Título: {titulo}, Usuário: {nome}, Data: {data}, Status: {status}\n")

    def mostrar_livros(self):
        livros = self.db.visualizar_livros()
        self.livros_text.delete(1.0, tk.END)
        for titulo, autor, isbn, disponivel in livros:
            status = "Disponível" if disponivel else "Emprestado"
            self.livros_text.insert(tk.END, f"Título: {titulo}, Autor: {autor}, ISBN: {isbn}, Status: {status}\n")

    def on_closing(self):
        self.db.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = BibliotecaApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
