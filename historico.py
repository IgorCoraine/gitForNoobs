import tkinter as tk
import git
import os
from tkinter import messagebox
from config import Config

class Historico(tk.Frame):
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
        
        self.label = tk.Label(self, text=f"Histórico de Commits: {self.repo_name}")
        self.label.pack()

        # Criação do frame para o Listbox e a barra de rolagem
        self.hist_frame = tk.Frame(self)
        self.hist_frame.pack(fill=tk.BOTH, expand=True)

        # Criação do Listbox
        self.commit_listbox = tk.Listbox(self.hist_frame)
        self.commit_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Criação da barra de rolagem
        self.scrollbar = tk.Scrollbar(self.hist_frame, orient="vertical", command=self.commit_listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill="y")

        # Configura o Listbox para usar a barra de rolagem
        self.commit_listbox.config(yscrollcommand=self.scrollbar.set)

        # Botão para restaurar o commit selecionado
        self.restore_button = tk.Button(self, text="Restaurar Estado", command=self.restore_commit)
        self.restore_button.pack(pady=10)

        self.load_history()

    def load_history(self):
        repo_path = os.path.join(self.base_path, self.repo_name)

        try:
            g = git.Repo(repo_path)
            commits = list(g.iter_commits())
            
            for commit in commits:
                commit_info = f"{commit.hexsha[:7]} - {commit.author.name} - {commit.committed_datetime} - {commit.message.strip()}"
                self.commit_listbox.insert(tk.END, commit_info)

        except Exception as e:
            print(f"Erro ao carregar histórico de commits: {e}")

    def restore_commit(self):
        """Restaura o estado do commit selecionado."""
        selected_index = self.commit_listbox.curselection()
        
        if not selected_index:
            messagebox.showwarning("Seleção Inválida", "Por favor, selecione um commit para ser restaurado.")
            return

        selected_commit = self.commit_listbox.get(selected_index)
        commit_id = selected_commit.split(" - ")[0]  # Pega apenas o ID do commit

        # Define o caminho para clonar o repositório
        base_path = Config.load_base_path()
        new_repo_name = f"{self.repo_name}_{commit_id}"
        new_repo_path = os.path.join(base_path, new_repo_name)

        try:
            # Clona o repositório original
            original_repo_path = os.path.join(base_path, self.repo_name)
            g_original = git.Repo(original_repo_path)

            # Clona o repositório na nova pasta
            g_clone = g_original.clone(new_repo_path)

            # Faz checkout do commit específico
            g_clone.git.checkout(commit_id)

            messagebox.showinfo("Estado Restaurado", f"Commit '{commit_id}' restaurado com sucesso em '{new_repo_path}'.")
        except Exception as e:
            messagebox.showerror("Erro ao Restaurar Commit", str(e))

