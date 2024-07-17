import tkinter as tk
from tkinter import messagebox
from datetime import datetime

class EstoqueDeCaixas:
    def __init__(self, root):
        self.root = root
        self.root.title("Controle de Estoque Alpha Carnes")

        self.caixas = {}

        # Título
        self.lbl_titulo = tk.Label(self.root, text="Controle de Estoque Alpha Carnes", font=("Helvetica", 16, "bold"))
        self.lbl_titulo.pack(pady=10)

        # Frames
        self.frame_entrada = tk.Frame(self.root)
        self.frame_entrada.pack(pady=10)

        self.frame_lista = tk.Frame(self.root)
        self.frame_lista.pack(pady=10)

        self.frame_botoes = tk.Frame(self.root)
        self.frame_botoes.pack(pady=10)

        # Entrada de Dados
        self.lbl_nome = tk.Label(self.frame_entrada, text="Nome da Caixa:")
        self.lbl_nome.grid(row=0, column=0, padx=5, pady=5)
        self.entry_nome = tk.Entry(self.frame_entrada)
        self.entry_nome.grid(row=0, column=1, padx=5, pady=5)

        self.lbl_quantidade = tk.Label(self.frame_entrada, text="Quantidade:")
        self.lbl_quantidade.grid(row=1, column=0, padx=5, pady=5)
        self.entry_quantidade = tk.Entry(self.frame_entrada)
        self.entry_quantidade.grid(row=1, column=1, padx=5, pady=5)

        self.lbl_data_entrada = tk.Label(self.frame_entrada, text="Data de Entrada (dd/mm/yyyy):")
        self.lbl_data_entrada.grid(row=2, column=0, padx=5, pady=5)
        self.entry_data_entrada = tk.Entry(self.frame_entrada)
        self.entry_data_entrada.grid(row=2, column=1, padx=5, pady=5)

        self.lbl_data_vencimento = tk.Label(self.frame_entrada, text="Data de Vencimento (dd/mm/yyyy):")
        self.lbl_data_vencimento.grid(row=3, column=0, padx=5, pady=5)
        self.entry_data_vencimento = tk.Entry(self.frame_entrada)
        self.entry_data_vencimento.grid(row=3, column=1, padx=5, pady=5)

        self.lbl_preco_custo = tk.Label(self.frame_entrada, text="Preço de Custo:")
        self.lbl_preco_custo.grid(row=4, column=0, padx=5, pady=5)
        self.entry_preco_custo = tk.Entry(self.frame_entrada)
        self.entry_preco_custo.grid(row=4, column=1, padx=5, pady=5)

        # Lista de Caixas
        self.lista_caixas = tk.Listbox(self.frame_lista, width=80)
        self.lista_caixas.pack()

        # Entrada de quantidade a ser removida
        self.lbl_quantidade_remover = tk.Label(self.frame_botoes, text="Quantidade para Remover:")
        self.lbl_quantidade_remover.grid(row=0, column=0, padx=5, pady=5)
        self.entry_quantidade_remover = tk.Entry(self.frame_botoes)
        self.entry_quantidade_remover.grid(row=0, column=1, padx=5, pady=5)

        # Botões
        self.btn_adicionar = tk.Button(self.frame_botoes, text="Adicionar Caixa", command=self.adicionar_caixa)
        self.btn_adicionar.grid(row=1, column=0, padx=5, pady=5)

        self.btn_remover = tk.Button(self.frame_botoes, text="Remover Caixa", command=self.remover_caixa)
        self.btn_remover.grid(row=1, column=1, padx=5, pady=5)

    def adicionar_caixa(self):
        nome = self.entry_nome.get()
        quantidade = self.entry_quantidade.get()
        data_entrada = self.entry_data_entrada.get()
        data_vencimento = self.entry_data_vencimento.get()
        preco_custo = self.entry_preco_custo.get()

        if not nome or not quantidade or not data_entrada or not data_vencimento or not preco_custo:
            messagebox.showwarning("Entrada Inválida", "Por favor, preencha todos os campos.")
            return

        try:
            quantidade = int(quantidade)
            preco_custo = float(preco_custo)
            datetime.strptime(data_entrada, "%d/%m/%Y")
            datetime.strptime(data_vencimento, "%d/%m/%Y")
        except ValueError:
            messagebox.showwarning("Entrada Inválida", "Verifique os valores inseridos.")
            return

        if nome in self.caixas:
            self.caixas[nome]['quantidade'] += quantidade
        else:
            self.caixas[nome] = {
                'quantidade': quantidade,
                'data_entrada': data_entrada,
                'data_vencimento': data_vencimento,
                'preco_custo': preco_custo
            }

        self.atualizar_lista()

        self.entry_nome.delete(0, tk.END)
        self.entry_quantidade.delete(0, tk.END)
        self.entry_data_entrada.delete(0, tk.END)
        self.entry_data_vencimento.delete(0, tk.END)
        self.entry_preco_custo.delete(0, tk.END)

    def remover_caixa(self):
        selecionado = self.lista_caixas.curselection()
        quantidade_remover = self.entry_quantidade_remover.get()

        if not selecionado:
            messagebox.showwarning("Seleção Inválida", "Por favor, selecione uma caixa para remover.")
            return

        if not quantidade_remover:
            messagebox.showwarning("Entrada Inválida", "Por favor, preencha a quantidade a ser removida.")
            return

        try:
            quantidade_remover = int(quantidade_remover)
        except ValueError:
            messagebox.showwarning("Entrada Inválida", "A quantidade a ser removida deve ser um número.")
            return

        nome = self.lista_caixas.get(selecionado).split(' - ')[0]

        if quantidade_remover >= self.caixas[nome]['quantidade']:
            del self.caixas[nome]
        else:
            self.caixas[nome]['quantidade'] -= quantidade_remover

        self.atualizar_lista()
        self.entry_quantidade_remover.delete(0, tk.END)

    def atualizar_lista(self):
        self.lista_caixas.delete(0, tk.END)
        for nome, detalhes in self.caixas.items():
            item = f"{nome} - Quantidade: {detalhes['quantidade']}, Entrada: {detalhes['data_entrada']}, Vencimento: {detalhes['data_vencimento']}, Preço: R${detalhes['preco_custo']:.2f}"
            self.lista_caixas.insert(tk.END, item)

if __name__ == "__main__":
    root = tk.Tk()
    app = EstoqueDeCaixas(root)
    root.mainloop()
