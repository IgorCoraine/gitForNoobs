import tkinter as tk
from tkinter import messagebox
import os
import git  # Importa a biblioteca GitPython
from PIL import Image, ImageTk  # Importa Image e ImageTk da biblioteca Pillow
from detalhes import Detalhes  # Importa a tela de detalhes
from config import Config

class Home(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

         # Carrega o caminho da pasta base
        self.base_path = Config.load_base_path()
        if not self.base_path:
            messagebox.showerror("Erro", "Não foi possível carregar o caminho da pasta base.")
            return

        # Criação da barra superior
        self.toolbar = tk.Frame(self)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        # Botão de Configuração
        self.config_button = tk.Button(self.toolbar, text="⚙️", command=self.show_config)
        self.config_button.pack(side=tk.LEFT, padx=5, pady=5)  # Adiciona o botão à barra
        #Botão de Atualizar página
        self.reload_button = tk.Button(self.toolbar, text="↻", command=self.update_repo_list)
        self.reload_button.pack(side=tk.LEFT, padx=5, pady=5)
        #Botão de Sobre
        self.reload_button = tk.Button(self.toolbar, text="Sobre", command=self.about)
        self.reload_button.pack(side=tk.RIGHT, padx=5, pady=5)

        self.label = tk.Label(self, text="Repositórios:")
        self.label.pack()

        # Criação do frame para o Listbox e a barra de rolagem
        self.frame = tk.Frame(self)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Criação do Listbox
        self.repo_listbox = tk.Listbox(self.frame)
        self.repo_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Criação da barra de rolagem
        self.scrollbar = tk.Scrollbar(self.frame, orient="vertical", command=self.repo_listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill="y")

        # Configura o Listbox para usar a barra de rolagem
        self.repo_listbox.config(yscrollcommand=self.scrollbar.set)

        # Frame para os botões
        self.button_frame = tk.Frame(self)
        self.button_frame.pack(pady=10)

        self.details_button = tk.Button(self.button_frame, text="Ver Detalhes", command=self.show_details)
        self.details_button.pack(side=tk.LEFT, padx=10)

        self.add_repo_button = tk.Button(self.button_frame, text="Adicionar Repositório", command=self.add_repository)
        self.add_repo_button.pack(side=tk.LEFT, padx=10)

        self.update_repo_list()

        # Variável para armazenar a referência da tela de detalhes
        self.detalhes_window = None
        self.config_window = None

    def update_repo_list(self):
        self.base_path = Config.load_base_path()
        if not self.base_path:
            messagebox.showerror("Erro", "Não foi possível carregar o caminho da pasta base.")
            return
        
        repos = [d for d in os.listdir(self.base_path) if os.path.isdir(os.path.join(self.base_path, d))]
        
        self.repo_listbox.delete(0, tk.END)  # Limpa a lista antes de atualizar
        for repo in repos:
            try:
                repo_path = os.path.join(self.base_path, repo)
                g = git.Repo(repo_path)
                status = "🔄" if g.is_dirty() else "✅"
                self.repo_listbox.insert(tk.END, f"{repo} - {status}")
            except Exception as e:
                status = "❌"
                self.repo_listbox.insert(tk.END, f"{repo} - {status}")

    def update_status(self):
        """Atualiza o status dos repositórios periodicamente."""
        self.update_repo_list()  # Chama o método para atualizar a lista de repositórios
        self.after(5000, self.update_status)  # Chama este método novamente após 5000 ms (5 segundos)

    def show_details(self):
        if self.config_window is not None:
            self.config_window.close_window()
        selected_repo_index = self.repo_listbox.curselection()
        if not selected_repo_index:
            messagebox.showwarning("Seleção Inválida", "Por favor, selecione um repositório.")
            return
        
        selected_repo = self.repo_listbox.get(selected_repo_index)
        repo_name = selected_repo.split(" - ")[0]  # Extrai o nome do repositório

        # Fecha a janela de detalhes anterior, se existir
        if self.detalhes_window is not None:
            self.detalhes_window.destroy()
            self.detalhes_window.close_history()

        # Cria uma nova janela de detalhes
        self.detalhes_window = Detalhes(self.master, repo_name)
        self.detalhes_window.pack(fill=tk.BOTH, expand=True)

    def add_repository(self):
        """Adiciona um novo repositório à pasta base."""
        # Cria uma janela popup para inserir o nome do novo repositório
        self.add_repo_popup = tk.Toplevel(self.master)
        self.add_repo_popup.title("Adicionar Repositório")

        tk.Label(self.add_repo_popup, text="Nome do Repositório:").pack(pady=5)
        self.repo_name_entry = tk.Entry(self.add_repo_popup, width=50)
        self.repo_name_entry.pack(pady=5)

        create_button = tk.Button(self.add_repo_popup, text="Criar Repositório", command=self.create_repository)
        create_button.pack(pady=10)

    def create_repository(self):
        repo_name = self.repo_name_entry.get().strip()
        if not repo_name:
            messagebox.showwarning("Nome Inválido", "Por favor, insira um nome para o repositório.")
            return

        base_path = Config.load_base_path()  # Carrega o caminho da pasta base
        if not base_path:
            messagebox.showerror("Erro", "Caminho da pasta base não encontrado.")
            return

        repo_path = os.path.join(base_path, repo_name)

        # Verifica se o repositório já existe
        if os.path.exists(repo_path):
            messagebox.showwarning("Repositório Já Existe", f"O repositório '{repo_name}' já existe.")
            return

        try:
            # Cria o diretório do novo repositório
            os.makedirs(repo_path)
            # Inicializa o repositório Git
            g = git.Repo.init(repo_path)

            messagebox.showinfo("Repositório Criado", f"Repositório '{repo_name}' criado com sucesso!")
            self.add_repo_popup.destroy()  # Fecha a janela popup após criar o repositório
            self.update_repo_list()  # Atualiza a lista de repositórios

        except Exception as e:
            messagebox.showerror("Erro ao Criar Repositório", str(e))


    def show_config(self):
        if self.detalhes_window is not None:
            self.detalhes_window.destroy()
            self.detalhes_window.close_history()
        self.config_window = Config(self.master)
        self.config_window.pack(fill=tk.BOTH, expand=True)

    def about(self):
        # Cria uma janela popup para colocar as informações do aplicativo
        self.about_popup = tk.Toplevel(self.master)
        self.about_popup.title("Sobre | Git For Noobs")

        # Define o tamanho da janela
        self.about_popup.geometry("350x300")  # Ajuste o tamanho conforme necessário

        # Adiciona labels com informações do aplicativo
        tk.Label(self.about_popup, text="Git For Noobs", font=("Arial", 16, "bold")).pack(pady=5, padx=10)

        tk.Label(self.about_popup, text="Version 1.0.0").pack(pady=5, padx=10)

        tk.Label(self.about_popup, text="Created by igor.coraine.github.io").pack(pady=5, padx=10)

        tk.Label(self.about_popup, text="This application is licensed under the MIT License.").pack(pady=5, padx=10)
        
        tk.Label(self.about_popup, text="Copyright (c) [2024] [Igor Coraine]").pack(pady=5, padx=10)

        # Carrega a imagem
        image_path = "/home/cora/Documentos/Dev/gitForNoobs/icon.png"  # Substitua pelo caminho da sua imagem
        try:
            original_image = Image.open(image_path)  # Abre a imagem original
            resized_image = original_image.resize((150, 150), Image.LANCZOS)  # Redimensiona a imagem (largura x altura)
            self.image = ImageTk.PhotoImage(resized_image)  # Converte para PhotoImage

            image_label = tk.Label(self.about_popup, image=self.image)  # Cria um label para a imagem
            image_label.pack()  # Adiciona o label da imagem ao popup
        except Exception as e:
            messagebox.showerror("Erro ao Carregar Imagem", str(e))
