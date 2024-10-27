from model.usuario import Usuario

class UsuarioController:
    def __init__(self):
        self.usuarios = []

    def cadastrar_usuario(self, nome, usuario_id):
        usuario = Usuario(nome, usuario_id)
        self.usuarios.append(usuario)
        return "Usuário cadastrado com sucesso!"
