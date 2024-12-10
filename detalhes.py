import tkinter as tk
import git
import os
from tkinter import messagebox
from historico import Historico  # Importa a tela de histórico

class Detalhes(tk.Frame):
    def __init__(self, master, repo_name):
        super().__init__(master)
        self.master = master
        self.repo_name = repo_name
        
        self.label = tk.Label(self, text=f"Detalhes do Repositório: {self.repo_name}")
        self.label.pack()

        self.file_listbox = tk.Listbox(self)
        self.file_listbox.pack(fill=tk.BOTH, expand=True)

        self.commit_button = tk.Button(self, text="Fazer Commit", command=self.commit_changes)
        self.commit_button.pack()

        self.history_button = tk.Button(self, text="Ver Histórico", command=self.show_history)
        self.history_button.pack()

        self.load_files()

    def load_files(self):
        base_path = "/home/cora/Documentos/Dev"  # Defina o caminho da pasta base aqui.
        repo_path = os.path.join(base_path, self.repo_name)

        # Verifica se o caminho é um repositório Git
        if not os.path.exists(os.path.join(repo_path, '.git')):
            messagebox.showwarning("Não é um repositório Git", f"A pasta '{self.repo_name}' não é um repositório Git.\nDeseja inicializar um novo repositório?")
            return  # Retorna se não for um repositório Git

        try:
            g = git.Repo(repo_path)
            # Lista todos os arquivos no diretório do repositório
            all_files = os.listdir(repo_path)
            tracked_files = g.git.ls_files().splitlines()  # Arquivos rastreados

            for file in all_files:
                if file == ".git":  # Ignora a pasta .git
                    continue
                
                file_path = os.path.join(repo_path, file)
                if os.path.isfile(file_path):
                    if file in tracked_files:
                        # Verifica se o arquivo foi modificado ou não
                        if g.is_dirty(untracked_files=True):
                            status = "✅" if g.index.diff(file) else "🔄"
                        else:
                            status = "✅"
                    else:
                        status = "🔄"  # Arquivo não rastreado

                    status_text = f"{file} - {status}"
                    self.file_listbox.insert(tk.END, status_text)

        except Exception as e:
            print(f"Erro ao carregar arquivos do repositório: {e}")

    def commit_changes(self):
        # Lógica para fazer commit; você pode adicionar um popup para inserir mensagem e user.name.
        pass

    def show_history(self):
        self.history_window = Historico(self.master, self.repo_name)
        self.history_window.pack(fill=tk.BOTH, expand=True)

    def close_history(self):
        # Fecha a janela de histórico anterior, se existir
        if self.history_window is not None:
            self.history_window.destroy()