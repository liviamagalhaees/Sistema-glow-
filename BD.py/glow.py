import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


def conectar():
    return sqlite3.connect('Glow.bd')

def criar_tabela():
    conn = conectar()
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS clientes(nome TEXT, telefone TEXT, imc TEXT)')
    conn.commit()
    conn.close()


def salvar():
    nome = entrada_nome.get()
    tel = entrada_tel.get()
    peso = entrada_peso.get()
    alt = entrada_altura.get()

    if nome and tel and peso and alt:
        try:
            imc = round(float(peso) / float(alt)**2, 2)
        except:
            messagebox.showerror('Erro', 'Peso ou altura inválidos!')
            return

        conn = conectar()
        c = conn.cursor()
        c.execute('INSERT INTO clientes VALUES (?,?,?)', (nome, tel, imc))
        conn.commit()
        conn.close()

        label_imc.config(text=str(imc))
        messagebox.showinfo('', f'CADASTRADO! IMC: {imc}')
        mostrar_clientes()
    else:
        messagebox.showwarning('', 'Preencha todos os campos!')

def mostrar_clientes():
    for i in tabela.get_children():
        tabela.delete(i)
    conn = conectar()
    c = conn.cursor()
    c.execute('SELECT * FROM clientes')
    for cliente in c.fetchall():
        tabela.insert('', 'end', values=cliente)
    conn.close()

def atualizar():
    selecionado = tabela.selection()
    if not selecionado:
        messagebox.showwarning('', 'Selecione um cliente!')
        return

    nome = entrada_nome.get()
    tel = entrada_tel.get()
    peso = entrada_peso.get()
    alt = entrada_altura.get()

    if not (nome and tel and peso and alt):
        messagebox.showwarning('', 'Preencha todos os campos!')
        return

    try:
        imc = round(float(peso) / float(alt)**2, 2)
    except:
        messagebox.showerror('Erro', 'Peso ou altura inválidos!')
        return

    conn = conectar()
    c = conn.cursor()
    c.execute("UPDATE clientes SET nome=?, telefone=?, imc=? WHERE nome=?",
              (nome, tel, imc, tabela.item(selecionado)['values'][0]))
    conn.commit()
    conn.close()

    label_imc.config(text=str(imc))
    messagebox.showinfo('', 'Atualizado!')
    mostrar_clientes()

def deletar():
    selecionado = tabela.selection()
    if selecionado:
        nome_cliente = tabela.item(selecionado)['values'][0]
        conn = conectar()
        c = conn.cursor()
        c.execute("DELETE FROM clientes WHERE nome=?", (nome_cliente,))
        conn.commit()
        conn.close()
        messagebox.showinfo('', 'Dado deletado!')
        mostrar_clientes()
    else:
        messagebox.showwarning('', 'Selecione um cliente!')

janela = tk.Tk()
janela.title('Cadastro Clinica Glow')
janela.geometry('600x320')
caminho = 'm_ico.ico'
janela.iconbitmap(caminho)

tk.Label(janela, text='Nome:').grid(row=0, column=0, pady=5)
entrada_nome = tk.Entry(janela)
entrada_nome.grid(row=0, column=1, pady=5)

tk.Label(janela, text='Telefone:').grid(row=1, column=0, pady=5)
entrada_tel = tk.Entry(janela)
entrada_tel.grid(row=1, column=1, pady=5)

tk.Label(janela, text='Peso (kg):').grid(row=2, column=0, pady=5)
entrada_peso = tk.Entry(janela)
entrada_peso.grid(row=2, column=1, pady=5)

tk.Label(janela, text='Altura (m):').grid(row=3, column=0, pady=5)
entrada_altura = tk.Entry(janela)
entrada_altura.grid(row=3, column=1, pady=5)

tk.Label(janela, text='IMC:').grid(row=4, column=0, pady=5)
label_imc = tk.Label(janela, text='', fg='blue')
label_imc.grid(row=4, column=1, pady=5)


tk.Button(janela, text='Salvar', command=salvar).grid(row=5, column=0, pady=10)
tk.Button(janela, text='Atualizar', command=atualizar).grid(row=5, column=1)
tk.Button(janela, text='Deletar', command=deletar).grid(row=5, column=6)


tabela = ttk.Treeview(janela, columns=('Nome', 'Telefone', 'IMC'), show='headings')
tabela.heading('Nome', text='Nome')
tabela.heading('Telefone', text='Telefone')
tabela.heading('IMC', text='IMC')
tabela.grid(row=8, column=10, columnspan=3, pady=20)


criar_tabela()
mostrar_clientes()
janela.mainloop()