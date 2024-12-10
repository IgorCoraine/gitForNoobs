import tkinter as tk
import git
import os

class Historico(tk.Frame):
    def __init__(self, master, repo_name):
        super().__init__(master)
        self.master = master
        self.repo_name = repo_name
        
        self.label = tk.Label(self, text=f"Histórico de Commits: {self.repo_name}")
        self.label.pack()

        self.commit_listbox = tk.Listbox(self)
        self.commit_listbox.pack(fill=tk.BOTH, expand=True)

        self.load_history()

    def load_history(self):
        base_path = "/home/cora/Documentos/Dev"  # Defina o caminho da pasta base aqui.
        repo_path = os.path.join(base_path, self.repo_name)

        try:
            g = git.Repo(repo_path)
            commits = list(g.iter_commits())
            
            for commit in commits:
                commit_info = f"{commit.hexsha[:7]} - {commit.author.name} - {commit.committed_datetime} - {commit.message.strip()}"
                self.commit_listbox.insert(tk.END, commit_info)

        except Exception as e:
            print(f"Erro ao carregar histórico de commits: {e}")
