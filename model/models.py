import sqlite3

class BibliotecaDB:
    def __init__(self, db_name="biblioteca.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.inicializar_tabelas()

    def inicializar_tabelas(self):
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
            return True
        except sqlite3.IntegrityError:
            return False

    def adicionar_usuario(self, nome, email):
        try:
            self.cursor.execute("INSERT INTO usuarios (nome, email) VALUES (?, ?)", (nome, email))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def emprestar_livro(self, livro_isbn, usuario_id):
        self.cursor.execute("SELECT disponivel FROM livros WHERE isbn = ?", (livro_isbn,))
        resultado = self.cursor.fetchone()
        if resultado and resultado[0] == 1:
            self.cursor.execute("INSERT INTO emprestimos (livro_isbn, usuario_id, data_emprestimo) VALUES (?, ?, datetime('now'))", (livro_isbn, usuario_id))
            self.cursor.execute("UPDATE livros SET disponivel = 0 WHERE isbn = ?", (livro_isbn,))
            self.conn.commit()
            return True
        return False

    def devolver_livro(self, livro_isbn):
        self.cursor.execute("SELECT disponivel FROM livros WHERE isbn = ?", (livro_isbn,))
        resultado = self.cursor.fetchone()
        if resultado and resultado[0] == 0:  
            self.cursor.execute("UPDATE livros SET disponivel = 1 WHERE isbn = ?", (livro_isbn,))
            self.cursor.execute("DELETE FROM emprestimos WHERE livro_isbn = ?", (livro_isbn,))
            self.conn.commit()
            return True
        return False

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
    
    def buscar_livro_por_isbn(self, isbn):
        self.cursor.execute("SELECT titulo, autor, isbn, disponivel FROM livros WHERE isbn = ?", (isbn,))
        livro = self.cursor.fetchone()
        
        if livro is None:
            return None
        
        return {
            "titulo": livro[0],
            "autor": livro[1],
            "isbn": livro[2],
            "disponivel": livro[3]
        }


    def close(self):
        self.conn.close()
