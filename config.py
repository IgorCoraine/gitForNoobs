import tkinter as tk
from tkinter import messagebox
import os

class Config(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        # Barra de divisão
        self.divider = tk.Frame(self, height=4, bg="black")
        self.divider.pack(fill=tk.X, pady=10)
        
        self.label = tk.Label(self, text="Configurações do Caminho da Pasta Base")
        self.label.pack(pady=10)

        self.path_label = tk.Label(self, text="Caminho da Pasta Base:")
        self.path_label.pack()

        self.path_entry = tk.Entry(self, width=50)
        self.path_entry.pack(pady=5)

        # Frame para os botões
        self.button_frame = tk.Frame(self)
        self.button_frame.pack(pady=10)

        # Botão para salvar as configurações
        self.save_button = tk.Button(self.button_frame, text="Salvar", command=self.save_config)
        self.save_button.pack(side=tk.LEFT, padx=10)

        # Botão para fechar as configurações
        self.close_button = tk.Button(self.button_frame, text="Cancelar", command=self.close_window)
        self.close_button.pack(side=tk.LEFT, padx=10)

        # Carrega o caminho atual da pasta base ao inicializar
        self.load_current_path()

    def load_current_path(self):
        """Carrega o caminho da pasta base a partir do arquivo de configuração e exibe no Entry."""
        if not os.path.exists("config.txt"):
            # Se o arquivo não existir, cria com um caminho padrão
            default_path = os.path.abspath(os.sep)  # Raiz do sistema (C:\ ou /)
            with open("config.txt", "w") as config_file:
                config_file.write(f"path={default_path}\n")  # Cria o arquivo com o caminho padrão
                print("Arquivo de configuração criado com o caminho padrão.")
        
        try:
            with open("config.txt", "r") as config_file:
                found_path = False
                for line in config_file:
                    if line.startswith("path="):
                        base_path = line.split("=")[1].strip()
                        self.path_entry.insert(0, base_path)  # Insere o caminho no Entry
                        found_path = True
                        break
                
                if not found_path:
                    # Se não encontrar 'path=', adiciona com um caminho padrão
                    default_path = os.path.abspath(os.sep)
                    with open("config.txt", "a") as config_file:
                        config_file.write(f"path={default_path}\n")
                    self.path_entry.insert(0, default_path)  # Insere o caminho padrão no Entry
                    print("Caminho padrão adicionado ao arquivo de configuração.")

        except Exception as e:
            print(f"Erro ao ler o arquivo de configuração: {e}")
            self.path_entry.delete(0, tk.END)  # Limpa o campo de entrada

    @staticmethod
    def load_base_path():
        """Carrega o caminho da pasta base a partir do arquivo de configuração."""
        try:
            if not os.path.exists("config.txt"):
                # Se o arquivo não existir, cria com um caminho padrão
                default_path = os.path.abspath(os.sep)  # Raiz do sistema (C:\ ou /)
                with open("config.txt", "w") as config_file:
                    config_file.write(f"path={default_path}\n")  # Cria o arquivo com o caminho padrão
                    print("Arquivo de configuração criado com o caminho padrão.")
            
            with open("config.txt", "r") as config_file:
                found_path = False
                for line in config_file:
                    if line.startswith("path="):
                        return line.split("=")[1].strip()
                
                if not found_path:
                    # Se não encontrar 'path=', adiciona com um caminho padrão
                    default_path = os.path.abspath(os.sep)
                    with open("config.txt", "a") as config_file:
                        config_file.write(f"path={default_path}\n")
                    return default_path

            return None

        except Exception as e:
            print(f"Erro ao ler o arquivo de configuração: {e}")
            return None

    def save_config(self):
        """Salva o caminho da pasta base em um arquivo de configuração."""
        base_path = self.path_entry.get().strip()
        
        if not os.path.isdir(base_path):
            messagebox.showwarning("Caminho Inválido", "Por favor, insira um caminho válido para a pasta base.")
            return

        with open("config.txt", "w") as config_file:
            config_file.write(f"path={base_path}\n")  # Salva o caminho no formato key=value

        messagebox.showinfo("Configuração Salva", "O caminho da pasta base foi salvo com sucesso!")
        self.close_window()

    def close_window(self):
        """Fecha a janela de configurações."""
        self.destroy()
