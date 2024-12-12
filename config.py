import tkinter as tk
from tkinter import messagebox
import os

class Config(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        
        self.label = tk.Label(self, text="Configurações do Caminho da Pasta Base")
        self.label.pack(pady=10)

        self.path_label = tk.Label(self, text="Caminho da Pasta Base:")
        self.path_label.pack()

        self.path_entry = tk.Entry(self, width=50)
        self.path_entry.pack(pady=5)

        # Botão para salvar as configurações
        self.save_button = tk.Button(self, text="Salvar", command=self.save_config)
        self.save_button.pack(pady=10)

        # Carrega o caminho atual da pasta base ao inicializar
        self.load_current_path()

    def load_current_path(self):
        """Carrega o caminho da pasta base a partir do arquivo de configuração e exibe no Entry."""
        try:
            with open("config.txt", "r") as config_file:
                base_path = config_file.read().strip()
                self.path_entry.insert(0, base_path)  # Insere o caminho no Entry
        except FileNotFoundError:
            print("Arquivo de configuração não encontrado.")
            # Se o arquivo não existir, podemos deixar o campo vazio ou definir um valor padrão
            self.path_entry.delete(0, tk.END)  # Limpa o campo de entrada

    @staticmethod
    def load_base_path():
        """Carrega o caminho da pasta base a partir do arquivo de configuração."""
        try:
            with open("config.txt", "r") as config_file:
                base_path = config_file.read().strip()
                return base_path
        except FileNotFoundError:
            print("Arquivo de configuração não encontrado.")
            return None

    def save_config(self):
        """Salva o caminho da pasta base em um arquivo de configuração."""
        base_path = self.path_entry.get().strip()
        
        if not os.path.isdir(base_path):
            messagebox.showwarning("Caminho Inválido", "Por favor, insira um caminho válido para a pasta base.")
            return

        with open("config.txt", "w") as config_file:
            config_file.write(base_path)  # Salva o caminho no arquivo

        messagebox.showinfo("Configuração Salva", "O caminho da pasta base foi salvo com sucesso!")
