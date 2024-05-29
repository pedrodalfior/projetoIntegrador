import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
import sqlite3
from datetime import datetime, timedelta
import customtkinter as ctk

class AlimentacaoApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Myhst - Seu sistema inteligente!")
        self.master.geometry("345x400")
        self.master.configure(bg="#f0f0f0")
        
        self.conectar_banco()
        self.criar_tabela()
        
        self.criar_widgets()

    def conectar_banco(self):
        self.conn = sqlite3.connect('alimentacao.db')
        self.cursor = self.conn.cursor()

    def criar_tabela(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS registros (
                            data TEXT,
                            alimentacao TEXT
                            )''')
        self.conn.commit()

    def criar_widgets(self):
        self.lbl_myhst = tk.Label(self.master, text="Myhst", bg="#f0f0f0", fg="#2c3e50", font=("Arial", 20))
        self.lbl_myhst.pack(pady=10)

        self.lbl_data = tk.Label(self.master, text="Selecione a data:", bg="#f0f0f0", fg="#2c3e50", font=("Arial", 12))
        self.lbl_data.pack(pady=5)

        self.cal_data = DateEntry(self.master, width=12, background='#2c3e50', foreground='white', borderwidth=2)
        self.cal_data.pack(pady=5)

        self.lbl_info = tk.Label(self.master, text="Insira sua alimentação:", bg="#f0f0f0", fg="#2c3e50", font=("Arial", 12))
        self.lbl_info.pack(pady=5)

        self.txt_alimentacao = tk.Text(self.master, height=5, width=40)
        self.txt_alimentacao.pack(pady=5)

        self.btn_registrar = ctk.CTkButton(self.master, text="Registrar", command=self.registrar_alimentacao, corner_radius=5)
        self.btn_registrar.pack(pady=10)

        self.btn_proxima_semana = ctk.CTkButton(self.master, text="Verificar Semana", command=self.verificar_semana, corner_radius=5)
        self.btn_proxima_semana.pack(pady=10)

    def registrar_alimentacao(self):
        data = self.cal_data.get_date()
        alimentacao = self.txt_alimentacao.get("1.0", tk.END).strip()

        if not alimentacao:
            messagebox.showwarning("Aviso", "Por favor, insira informações sobre sua alimentação.")
            return

        self.cursor.execute("SELECT * FROM registros WHERE data=?", (data,))
        registro_existente = self.cursor.fetchone()

        if registro_existente:
            messagebox.showwarning("Aviso", "Já existe um registro para esta data.")
            return

        self.cursor.execute("INSERT INTO registros (data, alimentacao) VALUES (?, ?)", (data, alimentacao))
        self.conn.commit()

        messagebox.showinfo("Sucesso", "Alimentação registrada com sucesso!")

    def verificar_semana(self):
        data_atual = datetime.now().date()
        data_inicio_semana = data_atual - timedelta(days=data_atual.weekday())
        data_fim_semana = data_inicio_semana + timedelta(days=6)

        self.cursor.execute("SELECT data, alimentacao FROM registros WHERE data BETWEEN ? AND ?", 
                            (data_inicio_semana, data_fim_semana))
        registros = self.cursor.fetchall()

        formulario = tk.Toplevel(self.master)
        formulario.title("Formulário de Alimentação da Semana")

        if registros:
            for data, alimentacao in registros:
                data_formatada = datetime.strptime(data, "%Y-%m-%d").strftime("%d/%m/%Y")
                lbl_data = tk.Label(formulario, text=f"Data: {data_formatada}", bg="#f0f0f0", fg="#2c3e50", font=("Arial", 12))
                lbl_data.pack()
                txt_alimentacao = tk.Text(formulario, height=5, width=40)
                txt_alimentacao.insert(tk.END, alimentacao)
                txt_alimentacao.pack()
        else:
            lbl_aviso = tk.Label(formulario, text="Não há registros para esta semana.", bg="#f0f0f0", fg="#2c3e50", font=("Arial", 12))
            lbl_aviso.pack()


def main():
    root = tk.Tk()
    root.configure(bg="#f0f0f0")
    app = AlimentacaoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
