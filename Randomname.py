import tkinter as tk
import random

# Dicionário de origens e suas respectivas listas de nomes masculinos e femininos
origens_nomes = {
    "Brasileira": {
        "Masculino": ["Arthur", "Bernardo", "Gabriel", "Gustavo", "Heitor", "João", "Júlio", "Luan", "Miguel", "Pedro", "Rafael", "Samuel", "Thiago", "Vitor", "William"],
        "Feminino":  ["Alice", "Beatriz", "Carolina", "Daniela", "Eduarda", "Fernanda", "Francisca", "Isabela", "Julia", "Lara", "Mariana", "Natália", "Patrícia", "Renata", "Sophia"]
    },
    "Celta": {
        "Masculino": ["Aidan", "Bran", "Cormac", "Dylan", "Eoin", "Fergus", "Gavin", "Liam", "Ronan", "Seamus", "Tadhg", "Niall", "Oscar", "Rory", "Eamon"],
        "Feminino": ["Brenna", "Cara", "Deirdre", "Fiona", "Gwyneth", "Isolde", "Maeve", "Niamh", "Orlaith", "Rhiannon", "Saoirse", "Siobhan", "Tegan", "Una", "Yseult"]
    },
    "USA": {
        "Masculino": ["Alexander", "Benjamin", "Daniel", "Ethan", "Henry", "Jacob", "Joseph", "Liam", "Matthew", "Michael", "Noah", "Ryan", "Samuel", "Thomas", "William"],
        "Feminino": ["Jennifer","Abigail", "Ava", "Charlotte", "Emily", "Grace", "Hannah", "Isabella", "Lily", "Mia", "Olivia", "Sophia", "Victoria", "Zoe", "Natalie", "Madison"]
    },
    "Africana": {
        "Masculino": ["Ade", "Amare", "Babatunde", "Chinedu", "Diallo", "Emeka", "Idris", "Kwame", "Lekan", "Oluwasegun", "Sadio", "Tariq", "Uzoma", "Yao", "Zuberi"],
        "Feminino": ["Amina", "Ayana", "Chioma", "Dalia", "Fatima", "Habiba", "Jamila", "Layla", "Malaika", "Nia", "Safiya", "Tatiana", "Zahara", "Zainab", "Zuri"]
    },
    "Japonesa": {
        "Masculino": ["Akira", "Daichi", "Haruki", "Hiroshi", "Kazuki", "Kenji", "Masashi", "Ryota", "Shinji", "Takahiro", "Takeshi", "Yoshiro", "Yuki", "Yusuke", "Zentaro"],
        "Feminino": ["Aiko", "Emi", "Hana", "Haruka", "Kazuko", "Kiyomi", "Mai", "Megumi", "Nanami", "Rina", "Sakura", "Tomoko", "Yoko", "Yumi", "Yuri"]
    }
}


# Configuração da janela principal
janela = tk.Tk()
janela.title("Gerador de Nomes para Bebês")
janela.configure(bg="light blue")

# Função para gerar um nome aleatório com base na origem e no gênero selecionados
def gerar_nome():
    genero = ""
    if var_genero.get() == 1:
        genero = "Masculino"
    else:
        genero = "Feminino"

    origem = var_origem.get()
    lista_nomes = origens_nomes[origem][genero]
    nome = random.choice(lista_nomes)
    label_nome.config(text=nome)

# Função para salvar o nome favorito na lista
def salvar_nome():
    nome_favorito = label_nome.cget("text")
    lista_favoritos.insert(tk.END, nome_favorito)

# Variáveis de controle para as opções selecionadas
var_origem = tk.StringVar(janela)
var_origem.set("Brasileira")

var_genero = tk.IntVar(janela)
var_genero.set(1)

# Menu suspenso para selecionar a origem
menu_origem = tk.OptionMenu(janela, var_origem, *origens_nomes.keys())
menu_origem.pack(pady=5)

# Botões de seleção de gênero
botao_masculino = tk.Radiobutton(janela, text="Masculino", variable=var_genero, value=1)
botao_masculino.pack()

botao_feminino = tk.Radiobutton(janela, text="Feminino", variable=var_genero, value=2)
botao_feminino.pack()

# Botão para gerar um nome aleatório
botao_gerar = tk.Button(janela, text="Gerar Nome", command=gerar_nome, width=15, bg="purple")
botao_gerar.pack(pady=5)



label_nome = tk.Label(janela, text="", font=("Arial", 18), bg="white")
label_nome.pack(pady=10)

lista_favoritos = tk.Listbox(janela, width=30)
lista_favoritos.pack(pady=10)

janela.mainloop()


