import flet as ft
import sqlite3
import bcrypt

# Configuração do banco de dados
def criar_tabela_usuarios():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha_hash TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('admin', 'user'))
    ''')
    conn.commit()
    conn.close()

# Cria um usuário admin padrão (apenas para exemplo)
def criar_admin_padrao():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    senha_hash = bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt())
    try:
        cursor.execute('INSERT INTO usuarios (username, senha_hash, role) VALUES (?, ?, ?)',
                       ("admin", senha_hash, "admin"))
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # Usuário já existe
    conn.close()

# Verifica credenciais
def verificar_login(username, senha):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT senha_hash, role FROM usuarios WHERE username = ?', (username,))
    resultado = cursor.fetchone()
    conn.close()
    
    if resultado and bcrypt.checkpw(senha.encode('utf-8'), resultado[0]):
        return resultado[1]  # Retorna o 'role'
    return None

# Interface Principal
def main(page: ft.Page):
    page.title = "Sistema de Autenticação"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    def rotear(route):
        page.views.clear()
        
        # Tela de Login
        if page.route == "/login":
            page.views.append(
                ft.View(
                    "/login",
                    [
                        ft.Text("Login", size=30, weight=ft.FontWeight.BOLD),
                        ft.TextField(label="Usuário", autofocus=True),
                        ft.TextField(label="Senha", password=True),
                        ft.ElevatedButton("Entrar", on_click=efetuar_login),
                        ft.Text("", color=ft.colors.RED)  # Para mensagens de erro
                    ]
                )
            )
        
        # Tela do Admin
        elif page.route == "/admin":
            page.views.append(
                ft.View(
                    "/admin",
                    [
                        ft.AppBar(title=ft.Text("Painel Admin"), bgcolor=ft.colors.BLUE),
                        ft.Text("Você tem acesso total!", size=20),
                        ft.ElevatedButton("Criar Post", on_click=criar_post),
                        ft.ElevatedButton("Sair", on_click=lambda _: page.go("/login"))
                    ]
                )
            )
        
        # Tela do Usuário
        elif page.route == "/user":
            page.views.append(
                ft.View(
                    "/user",
                    [
                        ft.AppBar(title=ft.Text("Conteúdo Público")),
                        ft.Text("Bem-vindo! Aqui estão os posts...", size=20),
                        ft.ElevatedButton("Sair", on_click=lambda _: page.go("/login"))
                    ]
                )
            )
        
        page.update()

    def efetuar_login(e):
        username = page.views[0].controls[1].value
        senha = page.views[0].controls[2].value
        role = verificar_login(username, senha)
        
        if role:
            page.session.set("user_role", role)
            page.go("/admin" if role == "admin" else "/user")
        else:
            page.views[0].controls[-1].value = "Credenciais inválidas!"
            page.update()

    def criar_post(e):
        # Lógica para criar posts (exemplo)
        dialog = ft.AlertDialog(title=ft.Text("Post criado com sucesso!"))
        page.dialog = dialog
        dialog.open = True
        page.update()

    # Inicialização
    criar_tabela_usuarios()
    criar_admin_padrao()
    page.on_route_change = rotear
    page.go("/login")

ft.app(target=main, view=ft.WEB_BROWSER)  # Para web; use `view=ft.AppView.FLET_APP` para desktop