import customtkinter as ctk
from tkinter import messagebox, filedialog, font
from fpdf import FPDF
from PIL import Image, ImageTk
import json
import webbrowser

# Configurações do customtkinter
ctk.set_appearance_mode("System")  # Pode ser "Light", "Dark", ou "System"
ctk.set_default_color_theme("blue")  # Tema base

# Criação da janela principal
janela = ctk.CTk()
janela.title("Urna eletrônica")

janela_largura = 800
janela_altura = 600

largura_tela = janela.winfo_screenwidth()
altura_tela = janela.winfo_screenheight()

posx = (largura_tela - janela_largura) // 2
posy = (altura_tela - janela_altura) // 2

# PDF
saida_pdf = FPDF()
saida_pdf.add_page()
saida_pdf.set_font('Arial', size=12)

# Carrega os candidatos
with open("candidatos.json", "r", encoding="utf-8") as arquivo:
    candidatos = json.load(arquivo)
votacao_ativa = False

# Fontes
fonte_titulo = ctk.CTkFont(family="Helvetica", size=40, weight="bold")
fonte_media = ctk.CTkFont(family="Helvetica", size=15, weight="bold")

# Mostra a tela inicial
def mostra_menu():
    janela.configure(padx=20, pady=60)
    janela.geometry(f"{janela_largura}x{janela_altura}+{posx}+{posy}")

    label_menu = ctk.CTkLabel(janela, text="Escolha uma opção:", font=fonte_titulo)
    label_menu.pack(pady=10)

    ctk.CTkButton(janela, text="Cadastro de Candidato", command=cadastra_candidato).pack(pady=20)
    ctk.CTkButton(janela, text="Iniciar Votação", command=iniciar_votacao).pack(pady=10)
    ctk.CTkButton(janela, text="Encerrar Votação", command=encerrar_votacao).pack(pady=10)

    janela.mainloop()

def exibir_imagens(tela, imagem_tk):
    label_imagem = ctk.CTkLabel(tela, image=imagem_tk, text="")
    label_imagem.image = imagem_tk
    label_imagem.pack(pady=5)

def carregar_imagem(caminho):
    imagem = Image.open(caminho)
    imagem_redimensionada = imagem.resize((200, 200))
    return ImageTk.PhotoImage(imagem_redimensionada)

def cadastra_candidato():
    janela.withdraw()
    janela_cadastro = ctk.CTkToplevel()
    janela_cadastro.protocol("WM_DELETE_WINDOW", janela.destroy)

    janela_cadastro.title("Cadastro de Candidato")
    janela_cadastro.geometry(f"{janela_largura}x{janela_altura}+{posx}+{posy}")

    ctk.CTkLabel(janela_cadastro, text="Número do Candidato:").pack(pady=5)
    entrada_numero = ctk.CTkEntry(janela_cadastro)
    entrada_numero.pack(pady=5)

    ctk.CTkLabel(janela_cadastro, text="Nome do Candidato:").pack(pady=5)
    entrada_nome = ctk.CTkEntry(janela_cadastro)
    entrada_nome.pack(pady=5)

    ctk.CTkLabel(janela_cadastro, text="Partido do Candidato:").pack(pady=5)
    entrada_partido = ctk.CTkEntry(janela_cadastro)
    entrada_partido.pack(pady=5)

    candidato_imgs = {"imagem_path": None, "imagem_tk": None}

    def escolher_imagem():
        caminho = filedialog.askopenfilename(
            title="Selecione uma imagem",
            filetypes=[("Imagens", "*.png *.jpg *.jpeg")]
        )
        if caminho:
            imagem_tk = carregar_imagem(caminho)
            candidato_imgs["imagem_path"] = caminho
            candidato_imgs["imagem_tk"] = imagem_tk
            exibir_imagens(janela_cadastro, imagem_tk)

    ctk.CTkButton(janela_cadastro, text="Escolher imagem", command=escolher_imagem).pack(pady=5)
    ctk.CTkButton(janela_cadastro, text="Voltar",
                  command=lambda: (janela_cadastro.destroy(), janela.deiconify())).pack(pady=5)

    def salvar_candidato():
        numero = entrada_numero.get()
        nome = entrada_nome.get()
        partido = entrada_partido.get()

        if numero.strip() == '' or nome.strip() == '' or partido.strip() == '':
            messagebox.showwarning("Erro", "Preencha todos os campos")
            return

        for c in candidatos:
            if c['numero'] == numero or c['partido'] == partido:
                if c['numero'] == numero and c['partido'] == partido:
                    menssagem = "Número e Partido do candidato já cadastrados."
                elif c['numero'] == numero:
                    menssagem = "Número do candidato já cadastrado."
                else:
                    menssagem = "Partido do candidato já cadastrado."

                messagebox.showwarning("Erro", menssagem)
                return

        candidatos.append({
            "numero": numero,
            "nome": nome,
            "partido": partido,
            "foto": candidato_imgs["imagem_path"] if candidato_imgs["imagem_path"] else None,
            "votos": 0
        })

        messagebox.showinfo("Sucesso", "Candidato cadastrado com sucesso!")

        janela_cadastro.destroy()
        cadastra_candidato()

        with open("candidatos.json", "w", encoding="utf-8") as arquivo:
            json.dump(candidatos, arquivo, indent=4, ensure_ascii=False)

    ctk.CTkButton(janela_cadastro, text="Salvar", command=salvar_candidato).pack(pady=5)

def iniciar_votacao():
    global votacao_ativa
    votacao_ativa = True
    registrar_voto()

def registrar_voto():
    if votacao_ativa:
        janela.withdraw()
        janela_votacao = ctk.CTkToplevel()
        janela_votacao.protocol("WM_DELETE_WINDOW", janela.destroy)

        janela_votacao.title("Votação")
        janela_votacao.geometry(f"{janela_largura}x{janela_altura}+{posx}+{posy}")

        ctk.CTkLabel(janela_votacao, text="Digite sua matrícula:").pack(pady=5)
        entrada_matricula = ctk.CTkEntry(janela_votacao)
        entrada_matricula.pack(pady=5)

        ctk.CTkLabel(janela_votacao, text="Digite o número do candidato:").pack(pady=5)
        entrada_voto = ctk.CTkEntry(janela_votacao)
        entrada_voto.pack(pady=5)

        ctk.CTkLabel(janela_votacao, text="Candidatos disponíveis:").pack(pady=5)

        def confirmar_voto():
            matricula = entrada_matricula.get()
            voto = entrada_voto.get()
            if not matricula:
                messagebox.showwarning("Erro", "Matrícula não pode ser vazia.")
                return
            candidato_escolhido = next((c for c in candidatos if c["numero"] == voto), None)
            if not candidato_escolhido:
                confirmar = messagebox.askyesno("Confirmação", "Candidato inexistente. Confirmar voto nulo?")
                if confirmar:
                    messagebox.showinfo("Sucesso", "Voto nulo registrado!")
                    janela_votacao.destroy()
                    registrar_voto()
                return

            confirmar = messagebox.askyesno(
                "Confirmação",
                f"Confirmar voto para {candidato_escolhido['nome']} ({candidato_escolhido['partido']})?"
            )

            if confirmar:
                candidato_escolhido["votos"] += 1
                messagebox.showinfo("Sucesso", "Voto registrado com sucesso!")
                janela_votacao.destroy()
                registrar_voto()

            with open("candidatos.json", "w", encoding="utf-8") as arquivo:
                json.dump(candidatos, arquivo, indent=4, ensure_ascii=False)

        ctk.CTkButton(janela_votacao, text="Votar", command=confirmar_voto).pack(pady=5)

        ctk.CTkButton(janela_votacao, text="Voltar",
                      command=lambda: (janela_votacao.destroy(), janela.deiconify())).pack(pady=5)

        # Frame com barra de rolagem
        frame_scroll = ctk.CTkFrame(janela_votacao)
        frame_scroll.pack(fill="both", expand=True, pady=10)

        canvas = ctk.CTkCanvas(frame_scroll, bg="#f0f0f0")
        scrollbar = ctk.CTkScrollbar(frame_scroll, orientation="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollable_frame = ctk.CTkFrame(canvas, fg_color="#f0f0f0")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for c in candidatos:
            frame_candidato = ctk.CTkFrame(scrollable_frame, fg_color="white")
            frame_candidato.pack(pady=5, fill="x", expand=True)

            if c["foto"]:
                imagem_tk = carregar_imagem(c["foto"])
                exibir_imagens(frame_candidato, imagem_tk)

            info = f"Número: {c['numero']}\nNome: {c['nome']}\nPartido: {c['partido']}"
            label_info = ctk.CTkLabel(frame_candidato, text=info, text_color="black")
            label_info.pack()

def imprime_relatorio():
    janela.withdraw()
    janela_relatorio = ctk.CTkToplevel()
    janela_relatorio.protocol("WM_DELETE_WINDOW", janela.destroy)

    janela_relatorio.title("Resultados")
    janela_relatorio.geometry(f"{janela_largura}x{janela_altura}+{posx}+{posy}")

    total_votos = sum(c["votos"] for c in candidatos)

    ctk.CTkButton(janela_relatorio, text="Voltar",
                  command=lambda: (janela.deiconify(), janela_relatorio.destroy())).pack(pady=5)

    if total_votos > 0:
        for candidato in candidatos:
            if candidato["foto"]:
                saida_pdf.image(candidato['foto'], 70, saida_pdf.get_y(), 50, 50)
            saida_pdf.cell(190, 10, txt=f"{candidato['nome']} ({candidato['partido']}): {candidato['votos']} votos", ln=True, align='C')
    else:
        saida_pdf.cell(190, 10, txt="Não houve votos válidos.", ln=True, align='C')

    def gerar_pdf():
        saida_pdf.output('Resultados_Votacao.pdf')
        webbrowser.open('Resultados_Votacao.pdf')

    ctk.CTkButton(janela_relatorio, text="Gerar PDF", command=gerar_pdf).pack(pady=5)

def encerrar_votacao():
    global votacao_ativa
    votacao_ativa = False
    imprime_relatorio()

mostra_menu()
