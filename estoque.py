import tkinter as tk

class Estoque:
    def __init__(self, master):
        self.master = master
        master.title("Controle de Estoque")

        # Criação das variáveis de estoque
        self.produto1 = tk.StringVar()
        self.produto2 = tk.StringVar()
        self.produto3 = tk.StringVar()

        # Criação dos rótulos e campos de entrada para cada produto
        tk.Label(master, text="Botas masculinas").grid(row=0)
        tk.Entry(master, textvariable=self.produto1).grid(row=0, column=1)
        tk.Label(master, text="Botas feminas").grid(row=1)
        tk.Entry(master, textvariable=self.produto2).grid(row=1, column=1)
        tk.Label(master, text="Sandálias femininas").grid(row=2)
        tk.Entry(master, textvariable=self.produto3).grid(row=2, column=1)
  

        # Criação dos botões para adicionar e remover estoque
        tk.Button(master, text="Adicionar", command=self.adicionar).grid(row=7, column=0, pady=10)
        tk.Button(master, text="Remover", command=self.remover).grid(row=7, column=1, pady=10)

        # Criação do rótulo para exibir a quantidade de estoque
        self.quantidade = tk.Label(master, text="")
        self.quantidade.grid(row=4, columnspan=2, pady=10)

    def adicionar(self):
        # Adiciona 1 unidade ao estoque de cada produto
        p1 = int(self.produto1.get()) + 1
        p2 = int(self.produto2.get()) + 1
        p3 = int(self.produto3.get()) + 1
        self.produto1.set(p1)
        self.produto2.set(p2)
        self.produto3.set(p3)
        self.exibir_quantidade()

    def remover(self):
        # Remove 1 unidade do estoque de cada produto, com verificação para não deixar ficar negativo
        p1 = max(0, int(self.produto1.get()) - 1)
        p2 = max(0, int(self.produto2.get()) - 1)
        p3 = max(0, int(self.produto3.get()) - 1)
        self.produto1.set(p1)
        self.produto2.set(p2)
        self.produto3.set(p3)
        self.exibir_quantidade()

    def exibir_quantidade(self):
        # Exibe a quantidade atual de cada produto em um rótulo
        quantidade = f"Botas masculinas: {self.produto1.get()} | Botas femininas: {self.produto2.get()} | Sandálias femininas: {self.produto3.get()}"
        self.quantidade.config(text=quantidade)

root = tk.Tk()
estoque = Estoque(root)
root.mainloop()
