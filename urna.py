import tkinter as tk
from tkinter import messagebox, filedialog, font
from fpdf import FPDF
from PIL import Image, ImageTk
import json
from datetime import datetime
import webbrowser

# Criação da janela pelo tkinter
janela = tk.Tk()
janela.title("Urna eletrônica") # Titulo da window aberta pelo Sistema Operacional

janela_largura = 800 # largura da window que se abre na tela
janela_altura = 600 # altura da window que se abre na tela
janela.resizable(False, False) # Impede alteração manual da largura e altura da janela

# Criação das váriaveis para centralizar a janela
largura_tela = janela.winfo_screenwidth() # largura da tela do usuário
altura_tela = janela.winfo_screenheight() # altura da tela do usuário

posx = (largura_tela - janela_largura) // 2 # Posição x da janela (ponto mais a esquerda da window)
posy = (altura_tela - janela_altura) // 2 # Posição y da janela (ponto mais alto da window)

# Criação da base do arquivo PDF que vai conter os resultados da votação
saida_pdf = FPDF() # Inicializa o arquivo onde será atribuid
saida_pdf.add_page() # Adciona uma página ao PDF

# Váriaveis para funcionalidade do código
with open("candidatos.json", "r", encoding="utf-8") as arquivo:
    candidatos = json.load(arquivo) # Abre o json e insere os dados dele em candidatos
votacao_ativa = False # Impede o usuário de ver os resultados antes de iniciar a votação

# Definição das fontes
fonte_titulo = font.Font(family="Helvetica", size=40, weight="bold")
fonte_media = font.Font(family="Helvetica", size=19, weight="bold")
fonte_pequena = font.Font(family="Helvetica", size=13)

# Mostra a tela inicial
def mostra_menu():
    # Definições básicas da janela atual
    janela.configure(bg="#f0f0f0", padx=20, pady=80) # Adiciona fundo cinza claro e margem grande
    janela.geometry(f"{janela_largura}x{janela_altura}+{posx}+{posy}") # Define a proporção e posição (centralizada) da janela

    label_menu = tk.Label(janela, text="Escolha uma opção:", width=18, height=2,
                          font=fonte_titulo) # "Caixa" p/ exibir texto ou imagem
    label_menu.pack(pady=10) # Espaçamento entre o rótulo e os botões

    frame_botoes = tk.Frame(janela, bg="#f0f0f0") # Container para alocar os botões em linha
    frame_botoes.pack(expand=True, pady=20) # Espaçamento vertical até o próximo widget na janela

    botao1 = tk.Button(frame_botoes, text="Cadastrar Candidatos", width=23, height=5, bg="#3d9dd4", fg="#ffffff",
                        font=fonte_pequena, command=cadastra_candidato) # Botão que chama função determinada ao clicar
    botao1.pack(side="left", padx=10, expand=True) # Botão alinhado a esquerda com um espaçamento horizontal

    botao2 = tk.Button(frame_botoes, text="Liberar Votação", width=23, height=5, bg="#45a755", fg="#ffffff",
                        font=fonte_pequena, command=liberar_votacao) # Linha 45
    botao2.pack(side="left", padx=10, expand=True) # Linha 46

    botao3 = tk.Button(frame_botoes, text="Ver Resultados", width=23, height=5, bg="#d49c14", fg="#ffffff",
                        font=fonte_pequena, command=ver_resultados) # Linha 45
    botao3.pack(side="left", padx=10, expand=True) # Linha 46

    janela.mainloop() # Mantém a janela rodando (sem isso ela abriria e fecharia logo em seguida, sem se quer ser visivel)

# Exibe uma imagem em uma das janelas
def exibir_imagens(tela, imagem_tk):
    label_imagem = tk.Label(tela) # Linha 42
    label_imagem.config(image=imagem_tk)
    label_imagem.image = imagem_tk # Garante que a imagem não se perde no parâmetro do Label
    label_imagem.pack(fill="both", expand=True)

# Carrega/Renderiza as imagens a partir do caminho delas
def carregar_imagem(caminho):
    imagem = Image.open(caminho) # Recebe um caminho de arquivo e o renderiza como iamgem

    imagem_redimensionada = imagem.resize((200, 150)) # Redimensiona, para tornar padrão
    
    return ImageTk.PhotoImage(imagem_redimensionada) # Retorna a imagem totalmente tratada

# Mostra a tela de cadastro de candidatos
def cadastra_candidato():
    janela.withdraw() # Esconde a janela inicial
    janela_cadastro = tk.Toplevel() # Cria um "filho" da var janela para ser exibido
    janela_cadastro.protocol("WM_DELETE_WINDOW", janela.destroy) # Caso o usuário feche a janela filha, o programa para

    # Definições básicas da janela atual
    janela_cadastro.title("Urna eletrônica") # Linha 9
    janela_cadastro.configure(bg='#f0f0f0', padx=30, pady=30) # Linha 39
    janela_cadastro.geometry(f"{janela_largura}x{janela_altura}+{posx}+{posy}") # linha 40
    janela_cadastro.resizable(False, False) # Linha 15

    # Conteúdo da janela atual
    def voltar():
        if entrada_nome.get() or entrada_numero.get() or entrada_partido.get():
            confirmar = messagebox.askyesno("Confirmação", "Existem dados não salvos, voltar mesmo assim?")
            if not confirmar:
                return
        janela_cadastro.destroy()
        janela.deiconify() # Pop-up de verificação para voltar caso haja input preenchido

    botao_voltar = tk.Button(janela_cadastro, text="Voltar", bg="#e11c1c", fg="#ffffff", font=fonte_pequena,
                                command=voltar) # Linha 45; Destrói janela atual e desesconde a principal
    botao_voltar.pack(anchor="e") # Linha 46

    label_menu = tk.Label(janela_cadastro, text="Insira as informações:", width=18, height=2,
                            font=fonte_titulo) # "Caixa" p/ exibir texto ou imagem
    label_menu.pack(pady=8) # Espaçamento entre o rótulo e os botões

    frame_geral = tk.Frame(janela_cadastro)
    frame_geral.pack(fill="x")

    frame_inputs = tk.Frame(frame_geral)
    frame_inputs.pack(expand=True, side="left", anchor="sw")

    tk.Label(frame_inputs, text="Número do Candidato:", font=fonte_pequena).pack(pady=6, anchor="w") # Linha 42
    entrada_numero = tk.Entry(frame_inputs, width=50) # Input que recebe "Número do Candidato"
    entrada_numero.pack(pady=6) # Linha 46

    tk.Label(frame_inputs, text="Nome do Candidato:", font=fonte_pequena).pack(pady=6, anchor="w") # Linha 42
    entrada_nome = tk.Entry(frame_inputs, width=50) # Input que recebe "Nome do Candidato"
    entrada_nome.pack(pady=6) # Linha 46

    tk.Label(frame_inputs, text="Partido do Candidato:", font=fonte_pequena).pack(pady=6, anchor="w") # Linha 42
    entrada_partido = tk.Entry(frame_inputs, width=50) # Input que recebe "Partido do Candidato"
    entrada_partido.pack(pady=6) # Linha 46
    
    # Dicionário para guardar as informações ultima imagem escolhida
    candidato_imgs = {
        "imagem_path": None,
        "imagem_tk": None
    }

    # Abre o gerenciador de arquivos para a escolha da imagem
    def escolher_imagem():
        caminho = filedialog.askopenfilename(
            title="Selecione uma imagem", # Titulo da janela do gerenciador de arquivos
            filetypes=[("Imagens", "*.png *.jpg *.jpeg")] # Legenda (à direita da barra de pequisa) e extensões escolhiveis
        )
        if caminho:
            imagem_tk = carregar_imagem(caminho) # Linha 86

            candidato_imgs["imagem_path"] = caminho # Guarda o caminho do arquivo da imagem atual
            candidato_imgs["imagem_tk"] = imagem_tk # Guarda a imagem renderizada atual

            exibir_imagens(container_imagem, imagem_tk) # Mostra a ultima imagem escolhida pelo usuário

    # Conteúdo da janela - Continuação
    frame_imagem = tk.Frame(frame_geral)
    frame_imagem.pack(expand=True, side="right", anchor="s")

    botao_imagem = tk.Button(frame_imagem, text="Escolher imagem:", bg="#d49c14", fg="#ffffff",
              font=fonte_pequena, command=escolher_imagem)
    botao_imagem.pack(pady=5) # Linha 45; Linha 46

    container_imagem = tk.Frame(frame_imagem, width=200, height=150)
    container_imagem.pack(pady=5)
    container_imagem.pack_propagate(False)

    # Salva as informações atuais na lista candidato como um candidato novo
    def salvar_candidato():
        # Pega os valores dos inputs
        numero = entrada_numero.get() # Recebe a string guardada em entada_numero
        nome = entrada_nome.get() # Recebe a string guardada em entada_nome
        partido = entrada_partido.get() # Recebe a string guardada em entada_partido

        # Verifica se algum input ficou vazio
        if numero.strip() == '' or nome.strip() == '' or partido.strip() == '':
            messagebox.showwarning("Erro", "Preencha todos os campos")
            return

        # Verifica se número ou partido do candidato é repetido
        for c in candidatos:
            if c['numero'] == numero or c['partido'] == partido:
                if c['numero'] == numero and c['partido'] == partido:
                    menssagem = "Número e Partido do candidato já cadastrados."
                elif c['numero'] == partido:
                    menssagem = "Número do candidato já cadastrado."
                else:
                    menssagem = "Partido do candidato já cadastrado."

                messagebox.showwarning("Erro", f"{menssagem}")
                return
        
        # Adciona os dados validados do candidato a lista dos candidatos 
        candidatos.append({"numero": numero,
                            "nome": nome,
                            "partido": partido,
                            "foto": candidato_imgs["imagem_path"] if candidato_imgs["imagem_path"] else None,
                            "votos": 0})

        messagebox.showinfo("Sucesso", "Candidato cadastrado com sucesso!") # Retorna menssagem em pop-up

        # Reseta a tela
        janela_cadastro.destroy()
        cadastra_candidato()

        # Por ultimo, reescreve o conteúdo do JSON
        with open("candidatos.json", "w", encoding="utf-8", ) as arquivo:
            json.dump(candidatos, arquivo, indent=4, ensure_ascii=False)

    botao_salvar = tk.Button(janela_cadastro, text="Salvar", width=16, height=3, bg="#45a755", fg="#ffffff",
              font=fonte_pequena, command=salvar_candidato)
    botao_salvar.pack(side="bottom", anchor="s") # Linha 45; Linha 46

# Inicia a votação e a formatação do PDF
def liberar_votacao():
    # Váriavel que permite a execução de registrar voto e impede encerrar votação sem iniciar antes
    global votacao_ativa
    votacao_ativa = True

    # Informações de tempo
    agora = datetime.now() # Tempo atual do mundo, mês, dia, ano, hora, minuto, segundo, milisegundos
    global data_votacao
    data_votacao = agora.date() # Apenas a data do tempo atual do mundo
    global inicio_votacao
    inicio_votacao = agora.strftime("%H:%M:%S") # Apenas as horas, minutos e segundos do tempo atual do mundo

    # Formatações do PDF
    saida_pdf.set_font('Arial', size=12) # Define a fonte a paritr desse ponto do PDF
    saida_pdf.cell(95, 20, txt=f"Data: {data_votacao}", ln=False, align="L") # Data no topo a esquerda
    saida_pdf.image("logo-je.png", 75, 10, 50)
    saida_pdf.cell(95, 20, txt=f"Inicio da votação: {inicio_votacao}", ln=True, align="R") # Hora no topo a direita
    saida_pdf.set_y(saida_pdf.get_y() + 10)
    saida_pdf.set_font('Arial', 'B', size=30) # Define a fonte a paritr desse ponto do PDF
    saida_pdf.cell(190, 40, txt="Resultados da votação:", ln=True, align="C") # Titulo centralizado abaixo das informações de tempo

    registrar_voto()

# Mostra os candidatos disponíveis e registra os votos do usuário 
def registrar_voto():
    if votacao_ativa:
        janela.withdraw() # Linha 65
        janela_votacao = tk.Toplevel() # Linha 66
        janela_votacao.protocol("WM_DELETE_WINDOW", janela.destroy) # Linha 67

        # Definições básicas da janela atual
        janela_votacao.title("Urna eletrônica") # Linha 9
        janela_votacao.configure(bg='#f0f0f0', padx=0, pady=30) # Linha 39
        janela_votacao.geometry(f"{janela_largura}x{janela_altura}+{posx}+{posy}") # linha 40
        janela_votacao.resizable(False, False) # Linha 15

        # Conteúdo da janela atual
        def voltar():
            if entrada_matricula.get() or entrada_voto.get():
                confirmar = messagebox.askyesno("Confirmação", "Existem dados não salvos, voltar mesmo assim?")
                if not confirmar:
                    return
            janela_votacao.destroy()
            janela.deiconify() # Pop-up de verificação para voltar caso haja input preenchido

        botao_voltar = tk.Button(janela_votacao, text="Voltar", bg="#e11c1c", fg="#ffffff", font=fonte_pequena,
                                    command=voltar) # Linha 45; Destrói janela atual e desesconde a principal
        botao_voltar.pack(padx=30, anchor="e") # Linha 46

        label_menu = tk.Label(janela_votacao, text="Realize seu voto:", width=18, height=2,
                                font=fonte_titulo) # "Caixa" p/ exibir texto ou imagem
        label_menu.pack(pady=8) # Espaçamento entre o rótulo e os botões

        # Frame que envolve toda a janela
        frame_principal = tk.Frame(janela_votacao)
        frame_principal.pack(fill="both", expand=True, pady=10)

        # Lado esquerdo
        frame_esquerda = tk.Frame(frame_principal)
        frame_esquerda.pack(side="left", expand=True)

        tk.Label(frame_esquerda, text="Digite sua matrícula:", font=fonte_pequena).pack(padx=10, pady=5, anchor="w") # Linha 42
        entrada_matricula = tk.Entry(frame_esquerda)
        entrada_matricula.pack(padx=10, pady=5, anchor="w")
        tk.Label(frame_esquerda, text="Digite o número do candidato:", font=fonte_pequena).pack(padx=10, pady=5, anchor="w") # Linha 42
        entrada_voto = tk.Entry(frame_esquerda)
        entrada_voto.pack(padx=10, pady=5, anchor="w")

    # Valida as informações e altera o JSON
    def confirmar_voto():
        matricula = entrada_matricula.get() # Linha
        voto = entrada_voto.get() # Linha
        if not matricula:
            messagebox.showwarning("Erro", "Matrícula não pode ser vazia.") # Linha
            return # Linha
        c_e = next((c for c in candidatos if c["numero"] == voto), None) # c_e = candidato de número igual ao voto
        if not c_e:
            messagebox.showwarning("Erro", "Número de candidato inválido.") # Linha
            return # Linha
        if c_e:
            confirmar = messagebox.askyesno("Confirmação",
                f"Confirmar voto para {c_e['nome']} ({c_e['partido']})?") # pop-up de confirmação (sim/não)

            # Finaliza operação de voto
            if confirmar:
                c_e["votos"] += 1
                messagebox.showinfo("Sucesso", "Voto registrado com sucesso!") # Linha
            else:
                confirmar = messagebox.askyesno("Confirmação", "Candidato inexistente. Confirmar voto nulo?")  # Linha
                if confirmar:
                    messagebox.showinfo("Sucesso", "Voto nulo registrado!")  # Linha

            # Linha
            janela_votacao.destroy()
            registrar_voto()

            # Linha 161
            with open("candidatos.json", "w", encoding="utf-8") as arquivo:
                json.dump(candidatos, arquivo, indent=4, ensure_ascii=False)

    # Linha
    botao_votar = tk.Button(janela_votacao, text="Votar", command=confirmar_voto, bg="green") # Linha 45
    botao_votar.pack(side="bottom", pady=10) # Linha

    # Lado direito
    frame_direita = tk.Frame(frame_principal)
    frame_direita.pack(side="right", expand=True)

    tk.Label(frame_direita, text="Candidatos disponiveis", font=fonte_pequena).pack(pady=5) # Linha 42

    # Frame com barra de rolagem para os candidatos
    frame_scroll = tk.Frame(frame_direita) # Cria um frame na janela
    frame_scroll.pack(fill="both", expand=True) # Definições de proporção do frame

    canvas = tk.Canvas(frame_scroll, bg="#f0f0f0") # Cria um canvas dentro do frame criado
    scrollbar = tk.Scrollbar(frame_scroll, orient="vertical", command=canvas.yview) # Cria uma scrollbar vertical que muda o y visivel
    canvas.configure(yscrollcommand=scrollbar.set) # Relaciona o canvas (conteúddo visivel) com o estado da scrollbar

    scrollable_frame = tk.Frame(canvas, bg="#f0f0f0") # Mais um frame (onde o conteúdo será inserido)
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    ) # Define toda a área do canvas como scrollavel

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="left", fill="y", anchor="ne")

    # Exibir os candidatos com imagem + texto
    for c in candidatos:
        frame_candidato = tk.Frame(scrollable_frame, bg="white", bd=1, relief="solid", padx=5, pady=5)
        frame_candidato.pack(pady=5, fill="x", expand=True)

        if c["foto"]:
            imagem_tk = carregar_imagem(c["foto"])
            exibir_imagens(frame_candidato, imagem_tk)

        info = f"Número: {c['numero']}\nNome: {c['nome']}\nPartido: {c['partido']}"
        label_info = tk.Label(frame_candidato, text=info, bg="white", justify="center") # Linha 42
        label_info.pack()

def imprime_relatorio():
    if not votacao_ativa:
        messagebox.showinfo("Erro", "A votação não pode ser encerrada antes de ser iniciada.")
        return
    janela.withdraw() # Linha 65
    janela_relatorio = tk.Toplevel() # Linha 66
    janela_relatorio.protocol("WM_DELETE_WINDOW", janela.destroy) # Linha 67

    # Definições básicas da janela atual
    janela_relatorio.title("Urna eletrônica") # Linha 9
    janela_relatorio.configure(bg='#f0f0f0', padx=30, pady=30) # linha 39
    janela_relatorio.geometry(f"{janela_largura}x{janela_altura}+{posx}+{posy}") # linha 40
    janela_relatorio.resizable(False, False) # Linha 15
    
    # Conteúdo da janela atual
    botao_voltar = tk.Button(janela_relatorio, text="Voltar", bg="#e11c1c", fg="#ffffff", font=fonte_pequena,
            command=lambda: (janela_relatorio.destroy(), janela.deiconify)) # Linha 45; Destrói janela atual e desesconde a principal
    botao_voltar.pack(anchor="e") # Linha 46

    total_votos = sum(c["votos"] for c in candidatos)

    # Preenche a página e o PDF com conteúdo
    if total_votos > 0:
        candidatos_ord = sorted(candidatos, key=lambda c: c["votos"], reverse=True)
        mais_votado = candidatos_ord[0]

        saida_pdf.set_font("Arial", size=12)
        saida_pdf.cell(190, 0, txt=f"{mais_votado['nome']} ({mais_votado['partido']}): {mais_votado['votos']} votos", ln=True, align='C')
        if mais_votado["foto"]:
            atual_y = saida_pdf.get_y()
            saida_pdf.image(mais_votado['foto'], 65, (atual_y+5), 80, 60)
            saida_pdf.set_y(atual_y + 70)

        outros_votados = candidatos_ord[1:]
        
        for i, candidato in enumerate(outros_votados):
            if saida_pdf.get_y() + 70 >= 4000:
                saida_pdf.add_page()
            alinhamento = 'L' if i % 2 == 0 else 'R'
            mudar_linha = True if alinhamento == 'R' else False
            posFoto = 10 if alinhamento == 'L' else 120
            saida_pdf.cell(95, 0, txt=f"{candidato['nome']} ({candidato['partido']}): {candidato['votos']} votos", ln=mudar_linha, align=alinhamento)
            if candidato["foto"]:
                atual_y = saida_pdf.get_y()
                saida_pdf.image(candidato['foto'], posFoto, (atual_y+5), 80, 60)
            else:
                # Retângulo cinza
                saida_pdf.set_fill_color(200, 200, 200)  # Cinza claro
                saida_pdf.rect(posFoto, (atual_y+5), 80, 60, 'F')  # 'F' = filled

                # Texto "Sem imagem" centralizado
                saida_pdf.set_xy(posFoto, (atual_y+5) + 60 / 2 - 5)  # Centralizado verticalmente
                saida_pdf.set_font("Arial", size=10)
                saida_pdf.cell(80, 10, "Sem imagem", border=0, ln=0, align='C')
            if alinhamento == 'R':
                saida_pdf.set_y(atual_y + 70)

    else:
        saida_pdf.set_font("Arial", size=20)
        saida_pdf.cell(190, 50, txt="Não houve votos válidos.", ln=True, align='C')

    def gerar_pdf():
        saida_pdf.output('Resultados_Votação.pdf')
        webbrowser.open('Resultados_Votação.pdf')

    tk.Button(janela_relatorio, text="Gerar PDF", command=gerar_pdf).pack() # Linha 45

def ver_resultados():
    global votacao_ativa
    imprime_relatorio()

mostra_menu()