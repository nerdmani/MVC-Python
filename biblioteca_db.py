import sqlite3

class BibliotecaDB:
    def __init__(self, db_name="biblioteca.db"):
        self.conn = sqlite3.connect(db_name)
        print("Conectado ao banco de dados SQLite")
        self.criar_tabela()

    def criar_tabela(self):
        query = """
        CREATE TABLE IF NOT EXISTS livros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            isbn TEXT UNIQUE NOT NULL,
            disponivel INTEGER DEFAULT 1
        )
        """
        self.conn.execute(query)
        self.conn.commit()
        print("Tabela 'livros' criada/verificada")

    def cadastrar_livro(self, titulo, autor, isbn):
        try:
            query = "INSERT INTO livros (titulo, autor, isbn) VALUES (?, ?, ?)"
            self.conn.execute(query, (titulo, autor, isbn))
            self.conn.commit()
            return "Livro cadastrado com sucesso!"
        except sqlite3.IntegrityError:
            return "Erro: ISBN já cadastrado."

    def consultar_livros(self, termo_busca=""):
        query = "SELECT * FROM livros WHERE titulo LIKE ? OR autor LIKE ?"
        cursor = self.conn.execute(query, (f"%{termo_busca}%", f"%{termo_busca}%"))
        return cursor.fetchall()

    def emprestar_livro(self, isbn):
        query = "UPDATE livros SET disponivel = 0 WHERE isbn = ? AND disponivel = 1"
        cursor = self.conn.execute(query, (isbn,))
        self.conn.commit()
        return cursor.rowcount > 0  # Retorna True se o empréstimo foi bem-sucedido

    def devolver_livro(self, isbn):
        query = "UPDATE livros SET disponivel = 1 WHERE isbn = ? AND disponivel = 0"
        cursor = self.conn.execute(query, (isbn,))
        self.conn.commit()
        return cursor.rowcount > 0  # Retorna True se a devolução foi bem-sucedida

