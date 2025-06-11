import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

#Banco de Dados
conn = sqlite3.connect('estante.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS obras (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL, 
        tipo TEXT NOT NULL,
        semana INTEGER NOT NULL,
        resenha TEXT
               )
''')
conn.commit()

#Funções
def salvar_obra():
    titulo = titulo_entry.get().strip()
    tipo = tipo_var.get()
    semana = semana_entry.get().strip()
    resenha = resenha_text.get("1.0", tk.END).strip()

    if not titulo or not tipo or not semana:
        messagebox.showwarning("Aviso", "Preencha todos os campos obrigatórios*.")
        return
    try:
        semana = int(semana)
        if not (1 <= semana <= 52):
            raise ValueError
    except ValueError:
        messagebox.showwarning("Aviso", "Semana deve ser um número entre 1 e 52.")
        return

    cursor.execute('''
        INSERT INTO obras (titulo, tipo, semana, resenha)
        VALUES (?, ?, ?, ?)
    ''', (titulo, tipo, semana, resenha))
    conn.commit()
    messagebox.showinfo("Sucesso", "Obra salva com sucesso!")
    limpar_campos()
    carregar_lista()

def limpar_campos():
    tipo_var.set("")
    titulo_entry.delete(0, tk.END)
    semana_entry.delete(0, tk.END)
    resenha_text.delete("1.0", tk.END)

def carregar_lista():
    lista.delete(*lista.get_children())
    cursor.execute("SELECT titulo, tipo, semana FROM obras ORDER BY semana")
    for row in cursor.fetchall():
        lista.insert("", tk.END, values=row)

#GUI
root = tk.Tk()
root.title("Minha Estante")

#título
tk.Label(root, text="*Título:").grid(row=0, column=0, sticky="w")
titulo_entry = tk.Entry(root)
titulo_entry.grid(row=1, column=1, pady=5, sticky="ew")

#tipo
tk.Label(root, text="*Tipo de Obra:").grid(row=1, column=0, sticky="w")
tipo_var = tk.StringVar()
tipo_combo = ttk.Combobox(root, textvariable=tipo_var, values=["Livro", "Quadrinho", "Mangá"], state="readonly")
tipo_combo.grid(row=0, column=1, pady=5, sticky="ew")

#semana
tk.Label(root, text="*Semana [1-52]:").grid(row=2, column=0, sticky="w")
semana_entry = tk.Entry(root)
semana_entry.grid(row=2, column=1, pady=5, sticky="ew")

#resenha
tk.Label(root, text="Resenha (opcional):").grid(row=3, column=0, sticky="nw")
resenha_text = tk.Text(root, height=4, width=40)
resenha_text.grid(row=3, column=1, pady=5, sticky="ew")

#botões
salvar_btn = tk.Button(root, text="Salvar", command=salvar_obra)
salvar_btn.grid(row=4, column=1, pady=10, sticky="e")

#lista
tk.Label(root, text="Obras Registradas:").grid(row=5, column=0, columnspan=2, sticky="w")
lista = ttk.Treeview(root, columns=("Título", "Tipo", "Semana"), show="headings")
for col in ("Título", "Tipo", "Semana"):
    lista.heading(col, text=col)
    lista.column(col, width=100)
lista.grid(row=6, column=0, columnspan=2, sticky="nsew", pady=5)


root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(6, weight=1)
carregar_lista()
root.mainloop()
