import tkinter as tk
from tkinter import messagebox, filedialog
from fpdf import FPDF
import webbrowser
from PIL import Image, ImageTk

# Criação da janela pelo tkinter
janela = tk.Tk()
janela.configure(bg="lightgray")
janela.title("Urna eletrônica")

# Definições para centralizar a janela
largura_tela = janela.winfo_screenwidth()
altura_tela = janela.winfo_screenheight()
posx = (largura_tela - 1200) // 2
posy = (altura_tela - 900) // 2

# Criação da base do arquivo PDF que vai conter os resultados da votação
saida_pdf = FPDF()
saida_pdf.add_page()
saida_pdf.set_font('Arial', size=12)

candidatos = []
imagens_candidatos = []
votacao_ativa = False

def mostra_menu():
    janela.geometry(f"1200x900+{posx}+{posy}") # Define o tamanho da janela principal
    janela.configure(padx=20, pady=20) # Adiciona margem grande
    label_menu = tk.Label(janela, text="Escolha uma opção:", bg="lightgray")
    label_menu.pack(pady=10) # Espaçamento entre o rótulo e os botões
    botao_cadastro = tk.Button(janela, text="Cadastro de Candidato", command=cadastra_candidato)
    botao_cadastro.pack(pady=5) # Espaçamento entre os botões
    botao_votacao = tk.Button(janela, text="Iniciar Votação", command=iniciar_votacao)
    botao_votacao.pack(pady=5)
    botao_encerrar = tk.Button(janela, text="Encerrar Votação", command=encerrar_votacao)
    botao_encerrar.pack(pady=5)
    janela.mainloop()

def exibir_imagem(tela):
        for i in imagens_candidatos:
            imagem = Image.open(i)

            image_tk = ImageTk.PhotoImage(imagem)


        imagem = Image.open(imagens_candidatos[-1])

        imagem_tk = ImageTk.PhotoImage(imagem)

        label_imagem = tk.Label(tela)
        label_imagem.config(image=imagem_tk)
        label_imagem.image = imagem_tk
        label_imagem.pack(pady=5)

def cadastra_candidato():
    janela_cadastro = tk.Toplevel(janela)
    janela_cadastro.title("Cadastro de Candidato")
    janela_cadastro.geometry(f"1200x900+{posx}+{posy}")
    janela_cadastro.configure(bg='lightgray')
    tk.Label(janela_cadastro, text="Número do Candidato:").pack(pady=5)
    entrada_numero = tk.Entry(janela_cadastro)
    entrada_numero.pack(pady=5)
    tk.Label(janela_cadastro, text="Nome do Candidato:").pack(pady=5)
    entrada_nome = tk.Entry(janela_cadastro)
    entrada_nome.pack(pady=5)
    tk.Label(janela_cadastro, text="Partido do Candidato:").pack(pady=5)
    entrada_partido = tk.Entry(janela_cadastro)
    entrada_partido.pack(pady=5)

    def escolher_imagem():
        caminho = filedialog.askopenfilename(
            title="Selecione uma imagem",
            filetypes=[("Imagens", "*.png *.jpg *.jpeg")]
        )
        if caminho:
            imagens_candidatos.append(caminho)
            exibir_imagem(janela_cadastro)

            imagem = Image.open(imagens_candidatos[-1])

            imagem_tk = ImageTk.PhotoImage(imagem)

            label_imagem = tk.Label(janela_cadastro)
            label_imagem.config(image=imagem_tk)
            label_imagem.image = imagem_tk
            label_imagem.pack(pady=5)

    entrada_imagem = tk.Button(janela_cadastro, text="Escolher imagem:", command=escolher_imagem)
    entrada_imagem.pack(pady=5)

    def salvar_candidato(foto):
        numero = entrada_numero.get()
        for c in candidatos:
            if c['numero'] == numero:
                messagebox.showwarning("Erro", "Número de candidato já cadastrado.")
                return
        nome = entrada_nome.get()
        partido = entrada_partido.get()
        foto = imagem
        candidatos.append({"numero": numero, "nome": nome, "partido": partido, "foto": foto, "votos": 0})

        messagebox.showinfo("Sucesso", "Candidato cadastrado com sucesso!")

        janela_cadastro.destroy()

    botao_salvar = tk.Button(janela_cadastro, text="Salvar", command=salvar_candidato)
    botao_salvar.pack(pady=5)

def iniciar_votacao():
    global votacao_ativa
    votacao_ativa = True
    registrar_voto()

def registrar_voto():
    if votacao_ativa:
        janela_votacao = tk.Toplevel(janela)
        janela_votacao.title("Votação")
        janela_votacao.geometry(f"1200x900+{posx}+{posy}")
        tk.Label(janela_votacao, text="Digite sua matrícula:").pack(pady=5)
        entrada_matricula = tk.Entry(janela_votacao)
        entrada_matricula.pack(pady=5)
        tk.Label(janela_votacao, text="Digite o número do candidato:").pack(pady=5)
        entrada_voto = tk.Entry(janela_votacao)
        entrada_voto.pack(pady=5)
        tk.Label(janela_votacao, text="Candidatos disponiveis").pack(pady=5)

    def confirmar_voto():
        matricula = entrada_matricula.get()
        voto = entrada_voto.get()
        if not matricula:
            messagebox.showwarning("Erro", "Matrícula não pode ser vazia.")
            return
        candidato_escolhido = next((c for c in candidatos if c["numero"] == voto), None)
        if not candidato_escolhido:
            messagebox.showwarning("Erro", "Número de candidato inválido.")
            return
        if candidato_escolhido:
            confirmar = messagebox.askyesno("Confirmação", f"Confirmar voto para {candidato_escolhido['nome']} ({candidato_escolhido['partido']})?")

            if confirmar:
                candidato_escolhido["votos"] += 1
                messagebox.showinfo("Sucesso", "Voto registrado com sucesso!")
                janela_votacao.destroy()
                registrar_voto()
            else:
                confirmar = messagebox.askyesno("Confirmação", "Candidato inexistente. Confirmar voto nulo?")
                if confirmar:
                    messagebox.showinfo("Sucesso", "Voto nulo registrado!")
                    janela_votacao.destroy()
                    registrar_voto()

    botao_votar = tk.Button(janela_votacao, text="Votar", command=confirmar_voto, bg="green")
    botao_votar.pack(pady=5)

    # Cria a Listbox e a Scrollbar
    listbox = tk.Listbox(janela_votacao, height=10, width=40)
    scrollbar = tk.Scrollbar(janela_votacao, orient="vertical", command=listbox.yview)

    # Conecta a Scrollbar à Listbox
    listbox.config(yscrollcommand=scrollbar.set)

    # Posiciona os widgets
    listbox.pack(pady=10, side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Preenche a lista com dados variáveis
    for i, c in enumerate(candidatos):
        final = "." if i == len(candidatos) - 1 else ";"
        listbox.insert(tk.END, f"Número: {c['numero']}, Nome: {c['nome']}, Partido: {c['partido']}{final}")

def imprime_relatorio():
    janela_relatorio = tk.Toplevel(janela)
    janela_relatorio.title("Resultados")
    janela_relatorio.geometry(f"1200x900+{posx}+{posy}")
    janela_relatorio.configure(bg='lightgray')
    total_votos = sum(c["votos"] for c in candidatos)
    if total_votos > 0:
        for candidato in candidatos:
            saida_pdf.cell(190, 10, txt=f"{candidato['nome']} ({candidato['partido']}):{candidato['votos']} votos", ln=True, align='C')
            saida_pdf.image()
    else:
        saida_pdf.cell(190, 10, txt="Não houve votos válidos.", ln=True, align='C')
        botao_fechar = tk.Button(janela_relatorio, text="Fechar", command=janela_relatorio.destroy)
        botao_fechar.pack(pady=5)
    saida_pdf.output('Resultados_Votação.pdf')
    webbrowser.open('Resultados_Votação.pdf')

def encerrar_votacao():
    global votacao_ativa
    votacao_ativa = False
    imprime_relatorio()

mostra_menu()