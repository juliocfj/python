import tkinter as tk
from tkinter import messagebox

# Lista de perguntas, opções e respostas
questions = [
    {
        "question": "Quem ganhou a Copa do Mundo de 2002?",
        "options": ["Brasil", "Alemanha", "Argentina", "França"],
        "answer": "Brasil",
    },
    {
        "question": "Qual jogador é conhecido como 'Rei do Futebol'?",
        "options": ["Maradona", "Pelé", "Zidane", "Cristiano Ronaldo"],
        "answer": "Pelé",
    },
    {
        "question": "Qual país sediou a Copa do Mundo de 2014?",
        "options": ["Brasil", "África do Sul", "Rússia", "Alemanha"],
        "answer": "Brasil",
    },
    {
        "question": "Qual clube italiano é maior campeão da Copa da Itália?",
        "options": ["Roma", "Juventus", "Milan", "Internazionale"],
        "answer": "Juventus",
    },
    {
        "question": "Qual jogador é conhecido como Imperador?",
        "options": ["Kaka", "Totti", "Adriano", "Júlio Cesar"],
        "answer": "Adriano",
    },
    {
        "question": "Quem é maior artilheiro do seculo 21 do Campeonato Inglês?",
        "options": ["Lampard", "Rooney", "Drogba", "Kane"],
        "answer": "Kane",
    },
]

current_question = 0
score = 0

def check_answer(selected_option, buttons):
    global current_question, score

    correct_answer = questions[current_question]["answer"]

    # Desabilitar os botões após a seleção
    for button in buttons:
        button["state"] = "disabled"

    # Verificar a resposta
    if selected_option == correct_answer:
        score += 1
        buttons[questions[current_question]["options"].index(selected_option)]["bg"] = "green"
    else:
        buttons[questions[current_question]["options"].index(selected_option)]["bg"] = "red"
        buttons[questions[current_question]["options"].index(correct_answer)]["bg"] = "green"

    # Perguntar se deseja continuar
    if messagebox.askyesno("Próxima pergunta", "Deseja continuar?"):
        next_question()
    else:
        messagebox.showinfo("Fim do Quiz", f"Você acertou {score} de {len(questions)} perguntas.")
        root.destroy()

def next_question():
    global current_question

    current_question += 1

    if current_question < len(questions):
        load_question()
    else:
        messagebox.showinfo("Fim do Quiz", f"Você acertou {score} de {len(questions)} perguntas.")
        root.destroy()

def load_question():
    for widget in frame.winfo_children():
        widget.destroy()

    question = questions[current_question]["question"]
    options = questions[current_question]["options"]

    question_label = tk.Label(
        frame, text=question, font=("Arial", 16, "bold"), fg="yellow", bg="green"
    )
    question_label.pack(pady=20)

    buttons = []
    for option in options:
        button = tk.Button(
            frame,
            text=option,
            font=("Arial", 14),
            bg="white",
            fg="black",
            command=lambda opt=option: check_answer(opt, buttons),
        )
        button.pack(pady=10, fill="x")
        buttons.append(button)

# Configuração da janela principal
root = tk.Tk()
root.title("Quiz de Futebol")
root.geometry("600x400")
root.configure(bg="green")

frame = tk.Frame(root, bg="green")
frame.pack(expand=True, fill="both")

load_question()
root.mainloop()
