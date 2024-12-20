import tkinter as tk
from tkinter import messagebox
import os
import hashlib

class Config(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        # Barra de divisão
        self.divider = tk.Frame(self, height=4, bg="black")
        self.divider.pack(fill=tk.X, pady=10)

        # Solicitar senha para acessar as configurações
        self.password_prompt()

    def password_prompt(self):
        """Solicita a senha para acessar as configurações."""
        self.password_window = tk.Toplevel(self.master)
        self.password_window.title("Autenticação")

        tk.Label(self.password_window, text="Digite a senha:").pack(pady=10)
        self.password_entry = tk.Entry(self.password_window, show='*', width=30)
        self.password_entry.pack(pady=5)

        submit_button = tk.Button(self.password_window, text="OK", command=self.check_password)
        submit_button.pack(pady=10)

    def check_password(self):
        """Verifica se a senha está correta."""
        entered_password = self.password_entry.get().strip()
        stored_hash = self.load_password_hash()

        if stored_hash is None:
            # Se não houver hash armazenado, cria um novo com a senha padrão
            default_password = "gitfornoobs"
            self.save_password_hash(default_password)
            messagebox.showinfo("Senha Criada", "Senha padrão foi criada.")
            self.password_window.destroy()
            self.setup_config_ui()  # Chama a configuração da interface
            return

        # Gera o hash da senha inserida
        entered_hash = hashlib.sha256(entered_password.encode()).hexdigest()

        if entered_hash == stored_hash:
            self.password_window.destroy()
            self.setup_config_ui()  # Chama a configuração da interface
        else:
            messagebox.showerror("Acesso Negado", "Senha incorreta. Tente novamente.")
            self.password_window.destroy()
            self.destroy()

    def load_password_hash(self):
        """Carrega o hash da senha do arquivo de configuração."""
        if not os.path.exists("config.txt"):
            return None
        
        try:
            with open("config.txt", "r") as config_file:
                for line in config_file:
                    if line.startswith("password="):
                        return line.split("=")[1].strip()
                return None
        except Exception as e:
            print(f"Erro ao ler o arquivo de configuração: {e}")
            return None

    def save_password_hash(self, password):
        """Salva ou atualiza o hash da senha no arquivo de configuração."""
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        # Lê o conteúdo atual do arquivo e atualiza o hash da senha
        lines = []
        
        if os.path.exists("config.txt"):
            with open("config.txt", "r") as config_file:
                lines = config_file.readlines()

        with open("config.txt", "w") as config_file:
            for line in lines:
                if line.startswith("password="):
                    config_file.write(f"password={hashed_password}\n")  # Atualiza a linha com o novo hash
                else:
                    config_file.write(line)  # Mantém as outras linhas inalteradas

    def setup_config_ui(self):
        """Configura a interface de configurações após autenticação."""
        tk.Label(self, text="Configurações do Caminho da Pasta Base").pack(pady=10)

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

        # Botão para fechar as configurações
        self.change_password_button = tk.Button(self, text="Alterar Senha", command=self.change_password)
        self.change_password_button.pack(pady=10)

        self.load_current_path()

    def change_password(self):
        """Solicita ao usuário que altere sua senha."""
        change_pass_window = tk.Toplevel(self.master)
        change_pass_window.title("Alterar Senha")

        tk.Label(change_pass_window, text="Senha Antiga:").pack(pady=5)
        old_pass_entry = tk.Entry(change_pass_window, show='*', width=30)
        old_pass_entry.pack(pady=5)

        tk.Label(change_pass_window, text="Nova Senha:").pack(pady=5)
        new_pass_entry = tk.Entry(change_pass_window, show='*', width=30)
        new_pass_entry.pack(pady=5)

        def update_password():
            old_password = old_pass_entry.get().strip()
            new_password = new_pass_entry.get().strip()

            if not old_password or not new_password:
                messagebox.showwarning("Campos Vazios", "Por favor, preencha todos os campos.")
                return

            stored_hash = self.load_password_hash()
            entered_hash = hashlib.sha256(old_password.encode()).hexdigest()

            if entered_hash == stored_hash:
                # Atualiza o hash da nova senha
                self.save_password_hash(new_password)
                messagebox.showinfo("Senha Alterada", "A senha foi alterada com sucesso!")
                change_pass_window.destroy()
            else:
                messagebox.showerror("Erro", "A senha antiga está incorreta.")

        update_button = tk.Button(change_pass_window, text="Alterar Senha", command=update_password)
        update_button.pack(pady=10)

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
        default_password = "gitfornoobs"
        hashed_password = hashlib.sha256(default_password.encode()).hexdigest()
        try:
            if not os.path.exists("config.txt"):
                # Se o arquivo não existir, cria com um caminho padrão
                default_path = os.path.abspath(os.sep)  # Raiz do sistema (C:\ ou /)
                with open("config.txt", "w") as config_file:
                    config_file.write(f"path={default_path}\n")  # Cria o arquivo com o caminho padrão
                    print("Arquivo de configuração criado com o caminho padrão.")
                    config_file.write(f"password={hashed_password}\n") #Cria o arquivo com a senha padrão
                    print("Arquivo de configuração criado com a senha padrão.")
            
            with open("config.txt", "r") as config_file:
                for line in config_file:
                    if line.startswith("path="):
                        return line.split("=")[1].strip()
                
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
        
    def close_window(self):
        """Fecha a janela de configurações."""
        self.destroy()
