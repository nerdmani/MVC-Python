import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

class BibliotecaView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.root.title("Sistema de Gerenciamento de Biblioteca")
        
        self.tabControl = ttk.Notebook(root)
        self.cadastro_livro_frame = ttk.Frame(self.tabControl)
        self.cadastro_usuario_frame = ttk.Frame(self.tabControl)
        self.emprestimo_frame = ttk.Frame(self.tabControl)
        self.visualizacao_emprestimos_frame = ttk.Frame(self.tabControl)
        self.visualizacao_livros_frame = ttk.Frame(self.tabControl)
        self.busca_livro_frame = ttk.Frame(self.tabControl)  
        
        # Adicionando as abas
        self.tabControl.add(self.cadastro_livro_frame, text='Cadastro de Livro')
        self.tabControl.add(self.cadastro_usuario_frame, text='Cadastro de Usuário')
        self.tabControl.add(self.emprestimo_frame, text='Empréstimos')
        self.tabControl.add(self.visualizacao_emprestimos_frame, text='Visualizar Empréstimos')
        self.tabControl.add(self.visualizacao_livros_frame, text='Visualizar Livros')
        self.tabControl.add(self.busca_livro_frame, text='Buscar Livro')  # Nova aba de busca
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

        self.adicionar_livro_btn = tk.Button(self.cadastro_livro_frame, text="Adicionar Livro", command=self.controller.adicionar_livro)
        self.adicionar_livro_btn.pack(pady=5)

        self.nome_entry = tk.Entry(self.cadastro_usuario_frame, width=30)
        self.nome_entry.insert(0, "Nome do Usuário")
        self.nome_entry.pack(pady=5)

        self.email_entry = tk.Entry(self.cadastro_usuario_frame, width=30)
        self.email_entry.insert(0, "Email do Usuário")
        self.email_entry.pack(pady=5)

        self.adicionar_usuario_btn = tk.Button(self.cadastro_usuario_frame, text="Adicionar Usuário", command=self.controller.adicionar_usuario)
        self.adicionar_usuario_btn.pack(pady=5)

        self.emprestar_btn = tk.Button(self.emprestimo_frame, text="Registrar Empréstimo", command=self.controller.registrar_emprestimo)
        self.emprestar_btn.pack(pady=10)

        self.devolver_btn = tk.Button(self.emprestimo_frame, text="Devolver Livro", command=self.controller.devolver_livro)
        self.devolver_btn.pack(pady=10)

        self.visualizar_emprestimos_btn = tk.Button(self.visualizacao_emprestimos_frame, text="Atualizar Lista de Empréstimos", command=self.controller.mostrar_emprestimos)
        self.visualizar_emprestimos_btn.pack(pady=10)
        self.emprestimos_text = tk.Text(self.visualizacao_emprestimos_frame, width=50, height=10)
        self.emprestimos_text.pack(pady=5)

        self.visualizar_livros_btn = tk.Button(self.visualizacao_livros_frame, text="Atualizar Lista de Livros", command=self.controller.mostrar_livros)
        self.visualizar_livros_btn.pack(pady=10)
        self.livros_text = tk.Text(self.visualizacao_livros_frame, width=50, height=10)
        self.livros_text.pack(pady=5)

        self.isbn_label = tk.Label(self.busca_livro_frame, text="ISBN:")
        self.isbn_label.pack(pady=5)
        self.isbn_entry = tk.Entry(self.busca_livro_frame)
        self.isbn_entry.pack(pady=5)

        self.buscar_button = tk.Button(self.busca_livro_frame, text="Buscar Livro", command=self.buscar_livro)
        self.buscar_button.pack(pady=5)

        self.resultado_label = tk.Label(self.busca_livro_frame, text="")
        self.resultado_label.pack(pady=5)

    def buscar_livro(self):
        isbn = self.isbn_entry.get()
        livro = self.controller.buscar_livro(isbn)
        
        if isinstance(livro, str):  
            self.mostrar_mensagem(livro)
        else:
            self.exibir_livro(livro)

    def exibir_livro(self, livro):
        if livro:
            print("Título:", livro["titulo"])
            print("Autor:", livro["autor"])
            print("ISBN:", livro["isbn"])
            print("Disponível:", "Sim" if livro["disponivel"] else "Não")
        else:
            print("Livro não encontrado.")