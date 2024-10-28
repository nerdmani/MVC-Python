import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

class BibliotecaDB:
    def __init__(self, db_name="biblioteca.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def adicionar_livro(self, titulo, autor, isbn):
        # Verifica se o ISBN já existe na tabela
        self.cursor.execute("SELECT * FROM livros WHERE isbn = ?", (isbn,))
        resultado = self.cursor.fetchone()
        
        if resultado:
            # Se o ISBN já existe, exibe uma mensagem de erro
            messagebox.showerror("Erro", "Este ISBN já está cadastrado.")
        else:
            # Caso contrário, insere o livro
            self.cursor.execute("INSERT INTO livros (titulo, autor, isbn) VALUES (?, ?, ?)", (titulo, autor, isbn))
            self.conn.commit()
            messagebox.showinfo("Sucesso", "Livro adicionado com sucesso!")

    def adicionar_usuario(self, nome, email):
        self.cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
        resultado = self.cursor.fetchone()

        if resultado:
            # Se o email já existe, exibe uma mensagem de erro
            messagebox.showerror("Erro", "Este email já está cadastrado.")
        else:
            # Caso contrário, insere o usuário
            self.cursor.execute("INSERT INTO usuarios (nome, email) VALUES (?, ?)", (nome, email))
            self.conn.commit()
            messagebox.showinfo("Sucesso", "Usuário adicionado com sucesso!")

    def emprestar_livro(self, livro_isbn, usuario_id):
        self.cursor.execute("INSERT INTO emprestimos (livro_isbn, usuario_id, data_emprestimo) VALUES (?, ?, datetime('now'))", (livro_isbn, usuario_id))
        self.conn.commit()

    def visualizar_emprestimos(self):
        self.cursor.execute("""
        SELECT l.titulo, u.nome, e.data_emprestimo 
        FROM emprestimos e 
        JOIN livros l ON e.livro_isbn = l.isbn 
        JOIN usuarios u ON e.usuario_id = u.id
        """)
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()

class BibliotecaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gerenciamento de Biblioteca")
        self.root.geometry("400x500")
        self.root.configure(bg="#f0f0f5")
        self.db = BibliotecaDB()

        self.create_widgets()

    def create_widgets(self):
        title_label = tk.Label(self.root, text="Biblioteca", font=("Helvetica", 18, "bold"), fg="#003366", bg="#f0f0f5")
        title_label.pack(pady=10)

        # Cadastro de livro
        livro_frame = tk.LabelFrame(self.root, text="Cadastro de Livro", font=("Helvetica", 12, "bold"), fg="#003366", bg="#f0f0f5", padx=10, pady=10)
        livro_frame.pack(padx=10, pady=10, fill="x")

        self.titulo_entry = tk.Entry(livro_frame, width=30)
        self.titulo_entry.insert(0, "Título do Livro")
        self.titulo_entry.pack(pady=5)

        self.autor_entry = tk.Entry(livro_frame, width=30)
        self.autor_entry.insert(0, "Autor do Livro")
        self.autor_entry.pack(pady=5)

        self.isbn_entry = tk.Entry(livro_frame, width=30)
        self.isbn_entry.insert(0, "ISBN do Livro")
        self.isbn_entry.pack(pady=5)

        self.adicionar_livro_btn = tk.Button(livro_frame, text="Adicionar Livro", command=self.adicionar_livro, bg="#4CAF50", fg="white", font=("Helvetica", 10, "bold"))
        self.adicionar_livro_btn.pack(pady=5)

        # Cadastro de usuário
        usuario_frame = tk.LabelFrame(self.root, text="Cadastro de Usuário", font=("Helvetica", 12, "bold"), fg="#003366", bg="#f0f0f5", padx=10, pady=10)
        usuario_frame.pack(padx=10, pady=10, fill="x")

        self.nome_entry = tk.Entry(usuario_frame, width=30)
        self.nome_entry.insert(0, "Nome do Usuário")
        self.nome_entry.pack(pady=5)

        self.email_entry = tk.Entry(usuario_frame, width=30)
        self.email_entry.insert(0, "Email do Usuário")
        self.email_entry.pack(pady=5)

        self.adicionar_usuario_btn = tk.Button(usuario_frame, text="Adicionar Usuário", command=self.adicionar_usuario, bg="#4CAF50", fg="white", font=("Helvetica", 10, "bold"))
        self.adicionar_usuario_btn.pack(pady=5)

        # Empréstimos
        self.emprestar_btn = tk.Button(self.root, text="Registrar Empréstimo", command=self.registrar_emprestimo, bg="#FF9800", fg="white", font=("Helvetica", 10, "bold"))
        self.emprestar_btn.pack(pady=10)

        # Visualizar Empréstimos
        self.visualizar_btn = tk.Button(self.root, text="Visualizar Empréstimos", command=self.visualizar_emprestimos, bg="#2196F3", fg="white", font=("Helvetica", 10, "bold"))
        self.visualizar_btn.pack(pady=10)

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
