import tkinter as tk
import git
import os

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

        self.load_files()

    def load_files(self):
        base_path = "/home/cora/Documentos/Dev"  # Defina o caminho da pasta base aqui.
        repo_path = os.path.join(base_path, self.repo_name)

        try:
            g = git.Repo(repo_path)
            for item in g.git.status(porcelain=True).splitlines():
                status_symbol = item[0]
                file_name = item[3:]  # O nome do arquivo começa após o espaço
                status_text = f"{status_symbol} {file_name}"
                self.file_listbox.insert(tk.END, status_text)
                
        except Exception as e:
            print(f"Erro ao carregar arquivos do repositório: {e}")

    def commit_changes(self):
        # Lógica para fazer commit; você pode adicionar um popup para inserir mensagem e user.name.
        pass
