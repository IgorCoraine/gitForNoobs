import tkinter as tk
from tkinter import messagebox
import os
import git  # Importa a biblioteca GitPython
from detalhes import Detalhes  # Importa a tela de detalhes

class Home(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        
        self.label = tk.Label(self, text="Repositórios:")
        self.label.pack()

        self.repo_listbox = tk.Listbox(self)
        self.repo_listbox.pack(fill=tk.BOTH, expand=True)

        self.details_button = tk.Button(self, text="Ver Detalhes", command=self.show_details)
        self.details_button.pack()

        self.add_repo_button = tk.Button(self, text="Adicionar Repositório", command=self.add_repository)
        self.add_repo_button.pack()

        self.update_repo_list()

        # Variável para armazenar a referência da tela de detalhes
        self.detalhes_window = None

    def update_repo_list(self):
        # Aqui você deve listar os repositórios na pasta base (definida em config)
        base_path = "/home/cora/Documentos/Dev"  # Defina o caminho da pasta base aqui.
        repos = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
        
        self.repo_listbox.delete(0, tk.END)  # Limpa a lista antes de atualizar
        for repo in repos:
            try:
                repo_path = os.path.join(base_path, repo)
                g = git.Repo(repo_path)
                status = "🔄" if g.is_dirty() else "✅"
                self.repo_listbox.insert(tk.END, f"{repo} - {status}")
            except Exception as e:
                print(f"Erro ao acessar o repositório {repo}: {e}")

    def update_status(self):
        """Atualiza o status dos repositórios periodicamente."""
        self.update_repo_list()  # Chama o método para atualizar a lista de repositórios
        self.after(5000, self.update_status)  # Chama este método novamente após 5000 ms (5 segundos)

    def show_details(self):
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
        # Função para adicionar um novo repositório
        new_repo_name = "novo_repositorio"  # Aqui você deve implementar a lógica para criar um novo repositório.
        messagebox.showinfo("Adicionar Repositório", f"Repositório '{new_repo_name}' criado com sucesso!")
