import tkinter as tk
import git
import os
from tkinter import messagebox
from historico import Historico  # Importa a tela de histórico
from config import Config

class Detalhes(tk.Frame):
    def __init__(self, master, repo_name):
        super().__init__(master)
        self.master = master
        self.repo_name = repo_name

        # Barra de divisão
        self.divider = tk.Frame(self, height=4, bg="black")
        self.divider.pack(fill=tk.X, pady=10)
        
        # Carrega o caminho da pasta base
        self.base_path = Config.load_base_path()
        if not self.base_path:
            messagebox.showerror("Erro", "Não foi possível carregar o caminho da pasta base.")
            return

        self.label = tk.Label(self, text=f"Detalhes do Repositório: {self.repo_name}")
        self.label.pack()

        # Criação do frame para o Listbox e a barra de rolagem
        self.frame = tk.Frame(self)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Criação do Listbox
        self.file_listbox = tk.Listbox(self.frame)
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Criação da barra de rolagem
        self.scrollbar = tk.Scrollbar(self.frame, orient="vertical", command=self.file_listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill="y")

        # Configura o Listbox para usar a barra de rolagem
        self.file_listbox.config(yscrollcommand=self.scrollbar.set)

        self.commit_button = tk.Button(self, text="Fazer Commit", command=self.commit_changes)
        self.commit_button.pack()

        self.history_button = tk.Button(self, text="Ver Histórico", command=self.show_history)
        self.history_button.pack()

        self.load_files()

        # Variável para armazenar a referência da tela de detalhes
        self.history_window = None

    def load_files(self):
        repo_path = os.path.join(self.base_path, self.repo_name)

        # Verifica se o caminho é um repositório Git
        if not os.path.exists(os.path.join(repo_path, '.git')):
            # Cria uma janela popup para perguntar se deseja criar um repositório no diretório existente
            self.add_repo_popup = tk.Toplevel(self.master)
            self.add_repo_popup.title("Não é um repositório Git")

            # Texto informativo
            message_label = tk.Label(self.add_repo_popup, text=f"A pasta '{self.repo_name}' não é um repositório Git.\nDeseja inicializar um novo repositório?")
            message_label.pack(pady=10)

            # Botão para criar o repositório
            create_button = tk.Button(self.add_repo_popup, text="Inicializar Repositório", command=lambda: self.create_repository(repo_path))
            create_button.pack(side=tk.LEFT, pady=10, padx=10)

            # Botão para não criar o repositório
            cancel_button = tk.Button(self.add_repo_popup, text="Cancelar", command=self.add_repo_popup.destroy)
            cancel_button.pack(side=tk.RIGHT, pady=10, padx=10)
            
        try:
            g = git.Repo(repo_path)
            all_files = os.listdir(repo_path)  # Lista todos os arquivos no diretório do repositório
            tracked_files = g.git.ls_files().splitlines()  # Arquivos rastreados
            modified_files = g.index.diff(None)  # Arquivos modificados

            for file in all_files:
                if file == ".git":  # Ignora a pasta .git
                    continue
                
                file_path = os.path.join(repo_path, file)
                if os.path.isfile(file_path):
                    if file in tracked_files:
                        # Verifica se o arquivo foi modificado ou não
                        if any(mod_file.a_path == file for mod_file in modified_files):
                            status = "🔄"  # Arquivo modificad
                        else:
                            status = "✅"  # Arquivo rastreado e não modificado
                    else:
                        status = "🔄"  # Arquivo não rastreado

                    status_text = f"{file} - {status}"
                    self.file_listbox.insert(tk.END, status_text)

        except Exception as e:
            self.config_window.close_window()
            print(f"Erro ao carregar arquivos do repositório: {e}")

    def create_repository(self, repo_path):
        """Cria um novo repositório Git no caminho especificado."""
        try:
            git.Repo.init(repo_path)  # Inicializa o repositório Git
            messagebox.showinfo("Repositório Criado", f"Repositório '{self.repo_name}' criado com sucesso!")
            self.add_repo_popup.destroy()  # Fecha a janela popup após criar o repositório
        except Exception as e:
            messagebox.showerror("Erro ao Criar Repositório", str(e))

    def commit_changes(self):
        # Cria uma janela popup para inserir a mensagem de commit
        commit_popup = tk.Toplevel(self.master)
        commit_popup.title("Fazer Commit")

        tk.Label(commit_popup, text="Mensagem do Commit:").pack()
        message_entry = tk.Entry(commit_popup, width=50)
        message_entry.pack()

        tk.Label(commit_popup, text="Nome do Autor:").pack()
        author_entry = tk.Entry(commit_popup, width=50)
        author_entry.pack()

        def perform_commit():
            message = message_entry.get()
            author_name = author_entry.get()

            if not message:
                messagebox.showwarning("Mensagem Vazia", "Por favor, insira uma mensagem de commit.")
                return
            if not author_name:
                messagebox.showwarning("Autor Vazio", "Por favor, insira um nome para o commit.")
                return

            repo_path = os.path.join("/home/cora/Documentos/Dev", self.repo_name)  # Defina o caminho da pasta base aqui.
            try:
                g = git.Repo(repo_path)

                # Adiciona todos os arquivos modificados ao índice
                g.git.add(A=True)  # Adiciona todos os arquivos

                # Realiza o commit
                g.config_writer().set_value("user", "name", author_name).release()
                g.index.commit(message)

                messagebox.showinfo("Commit Realizado", "As alterações foram comitadas com sucesso.")
                commit_popup.destroy()  # Fecha a janela popup após o commit
            except Exception as e:
                messagebox.showerror("Erro ao Fazer Commit", str(e))

        commit_button = tk.Button(commit_popup, text="Commit", command=perform_commit)
        commit_button.pack()


    def show_history(self):
        # Fecha a janela de detalhes anterior, se existir
        if self.history_window is not None:
            self.history_window.destroy()

        self.history_window = Historico(self.master, self.repo_name)
        self.history_window.pack(fill=tk.BOTH, expand=True)

        # Remove o botão de histórico
        self.history_button.pack_forget() 

    def close_history(self):
        # Fecha a janela de histórico anterior, se existir
        try:
            if self.history_window is not None:
                self.history_window.destroy()
        except:
            pass
        