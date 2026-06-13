import customtkinter as ctk
from tkinter import filedialog, messagebox
import pandas as pd
import os

# Configuração visual do aplicativo
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class AppDiario(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Gerador do Conselho de Classe - CIEP 205")
        self.geometry("500x300")
        self.resizable(False, False)
        
        # Título na tela
        self.label_titulo = ctk.CTkLabel(self, text="Painel Automação - Diário Docente", font=("Arial", 20, "bold"))
        self.label_titulo.pack(pady=20)
        
        # Texto de instrução
        self.label_instrucao = ctk.CTkLabel(self, text="Selecione o arquivo .csv baixado do sistema escolar:", font=("Arial", 14))
        self.label_instrucao.pack(pady=10)
        
        # Botão principal
        self.btn_gerar = ctk.CTkButton(self, text="Selecionar Diário e Gerar Excel", command=self.processar_diario, font=("Arial", 14, "bold"), height=45)
        self.btn_gerar.pack(pady=20)
        
        # Rodapé
        self.label_rodape = ctk.CTkLabel(self, text="Pronto para uso", font=("Arial", 11, "italic"), text_color="gray")
        self.label_rodape.pack(side="bottom", pady=10)

    def processar_diario(self):
        # Abre a janela para você escolher o arquivo de onde ele estiver
        arquivo_origem = filedialog.askopenfilename(
            title="Escolha o arquivo do Diário de Classe",
            filetypes=[("Arquivos CSV", "*.csv")]
        )
        
        if not arquivo_origem:
            return # Se o usuário cancelar, não faz nada
            
        try:
            self.label_rodape.configure(text="Processando dados...", text_color="orange")
            self.update()
            
            # Lê o arquivo que você escolheu com o separador correto
            df_notas = pd.read_csv(arquivo_origem, sep=";", encoding="utf-8-sig")
            
            # Define onde vai salvar (na mesma pasta 'deder')
            pasta_destino = os.path.dirname(os.path.abspath(__file__))
            caminho_final = os.path.join(pasta_destino, "Consolidado_Bimestre_CIEP_205.xlsx")
            
            # Gera o Excel
            df_notas.to_excel(caminho_final, index=False, sheet_name="Fechamento_Bimestre")
            
            self.label_rodape.configure(text="Arquivo gerado com sucesso!", text_color="green")
            
            # Abre uma caixinha de aviso de sucesso na tela
            messagebox.showinfo("🏆 Sucesso!", f"O arquivo do Conselho foi gerado com sucesso na pasta:\n\n{caminho_final}")
            
        except Exception as e:
            self.label_rodape.configure(text="Erro ao processar.", text_color="red")
            messagebox.showerror("❌ Erro", f"Não foi possível processar o arquivo:\n{e}")

if __name__ == "__main__":
    app = AppDiario()
    app.mainloop()